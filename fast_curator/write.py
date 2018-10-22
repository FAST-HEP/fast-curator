from __future__ import print_function
import itertools
import operator
import os
from fast_curator import read
from collections import defaultdict
import logging
logger = logging.getLogger(__name__)


class UsingUproot():
    import uproot
    from . import xrootd_glob

    @staticmethod
    def expand_file_list(files):
        full_list = []
        for name in files:
            expanded = UsingUproot.xrootd_glob.glob(name)
            full_list += [str(exp) for exp in expanded]
        return full_list

    @staticmethod
    def total_entries(files, tree):
        return UsingUproot.uproot.numentries(files, tree)


class UsingROOT():

    @staticmethod
    def expand_file_list(files):
        from rootpy.utils.ext_glob import glob
        full_list = []
        for name in files:
            expanded = glob(name)
            full_list += [str(exp) for exp in expanded]
        return full_list

    @staticmethod
    def total_entries(files, tree):
        from rootpy import ROOT
        chain = ROOT.TChain(tree)
        for _file in files:
            chain.Add(_file)
        return chain.GetEntries()


def prepare_file_list(files, dataset, eventtype, tree_name, use_uproot=True, absolute_paths=True):
    """
    Expands all globs in the file lists and creates a dataframe similar to those from a DAS query
    """

    process_files = UsingUproot if use_uproot else UsingROOT
    full_list = process_files.expand_file_list(files)
    if absolute_paths:
        full_list = [os.path.realpath(f) if ':' not in f else f for f in full_list]
    numentries = process_files.total_entries(full_list, tree_name)

    data = {}
    data["eventtype"] = eventtype
    data["name"] = dataset
    data["nevents"] = numentries
    data["nfiles"] = len(full_list)
    data["files"] = full_list
    data["tree"] = tree_name

    return data


def select_default(values):
    groups = itertools.groupby(sorted(values))
    groups = [(group, sum(1 for _ in items)) for group, items in groups]
    groups = [group for group in groups if group[1] > 1]
    if not groups:
        return None
    most_common, number_items = max(groups, key=operator.itemgetter(1))
    is_unique = len(map(lambda x: x[1] == number_items, groups)) == 1
    if not is_unique:
        return None
    return most_common


def prepare_contents(datasets):
    datasets = [vars(data) if isinstance(data, read.Dataset)
                else data for data in datasets]
    for d in datasets:
        if "associates" in d:
            del d["associates"]

    # build the default properties
    values = defaultdict(list)
    for data in datasets:
        for k, v in data.items():
            values[k].append(v)

    defaults = {}
    for key, vals in values.items():
        if key == "name":
            continue
        is_in_all_datasets = len(vals) == len(datasets)
        if not is_in_all_datasets:
            continue
        new_default = select_default(vals)
        if new_default:
            defaults[key] = new_default

    cleaned_datasets = []
    for data in datasets:
        new_data = {}
        for key, val in data.items():
            if key in defaults and val == defaults[key]:
                continue
            new_data[key] = val
        cleaned_datasets.append(new_data)

    contents = dict(datasets=cleaned_datasets)
    if defaults:
        contents["defaults"] = defaults
    return contents


def write_yaml(dataset, out_file):
    import yaml
    if os.path.exists(out_file):
        datasets = read.from_yaml(out_file)
        datasets.append(dataset)
        contents = prepare_contents(datasets)
    else:
        contents = {}
        contents["datasets"] = [dataset]

    # https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

    yaml_contents = yaml.dump(
        contents, Dumper=MyDumper, default_flow_style=False)
    with open(out_file, 'w') as out:
        out.write(yaml_contents)
    print(yaml_contents)

    return contents


def add_meta(dataset, meta):
    for key, value in meta:
        if key in meta:
            msg = "Meta data '%s' will override an existing value" % key
            raise RuntimeError(msg)
        dataset[key] = value
