from __future__ import print_function
import six
import itertools
import operator
import os
from . import read
from .catalogues import get_file_list_expander, known_expanders
from collections import defaultdict
import logging
logger = logging.getLogger(__name__)


__all__ = ["known_expanders", "prepare_file_list", "write_yaml",
           "add_meta", "process_user_function"]


def prepare_file_list(files, dataset, eventtype, tree_name, expand_files="xrootd",
                      prefix=None, no_empty_files=True, confirm_tree=True,
                      ignore_inaccessible=False,
                      include_branches=False):
    """
    Expands all globs in the file lists and creates a dataframe similar to those from a DAS query
    """
    if isinstance(expand_files, six.string_types):
        expand_files = get_file_list_expander(expand_files)
    if isinstance(files, six.string_types):
        files = [files]
    full_list = expand_files.expand_file_list(files, prefix=prefix)
    full_list = [os.path.realpath(f) if ':' not in f else f for f in full_list]
    full_list, numentries, branches = expand_files.check_files(full_list, tree_name,
                                                               no_empty=no_empty_files,
                                                               list_branches=include_branches,
                                                               confirm_tree=confirm_tree,
                                                               ignore_inaccessible=ignore_inaccessible)

    data = {}
    if prefix:
        full_list = ["{prefix}" + path[len(prefix):] if path.startswith(prefix) else path for path in full_list]
        data["prefix"] = [{"default": prefix}]
    data["eventtype"] = eventtype
    data["name"] = dataset
    data["nevents"] = numentries
    data["nfiles"] = len(full_list)
    data["files"] = full_list
    data["tree"] = tree_name[0] if len(tree_name) == 1 else tree_name
    if branches:
        data["branches"] = branches

    return data


def select_default(values):
    groups = itertools.groupby(sorted(values))
    groups = [(group, sum(1 for _ in items)) for group, items in groups]
    groups = [group for group in groups if group[1] > 1]
    if not groups:
        return None
    most_common, number_items = max(groups, key=operator.itemgetter(1))
    is_unique = sum([1 for group in groups if group[1] == number_items]) == 1
    if not is_unique:
        return None
    return most_common


def prepare_contents(datasets, no_defaults_in_output=False):
    datasets = [vars(data) if isinstance(data, read.Dataset)
                else data for data in datasets]
    for d in datasets:
        if "associates" in d:
            del d["associates"]

    if no_defaults_in_output:
        # do not group common settings together in default block
        return dict(datasets=datasets)

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


def write_yaml(dataset, out_file, append=True, no_defaults_in_output=False):
    import yaml
    if os.path.exists(out_file) and append:
        datasets = read.from_yaml(out_file, expand_prefix=False)
        datasets.append(dataset)
        contents = prepare_contents(datasets, no_defaults_in_output=no_defaults_in_output)
    else:
        contents = {}
        contents["datasets"] = [dataset]

    # https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
    class MyDumper(yaml.Dumper):
        def increase_indent(self, flow=False, indentless=False):
            return super(MyDumper, self).increase_indent(flow, False)

        # disable aliases and anchors, see https://github.com/yaml/pyyaml/issues/103
        def ignore_aliases(self, data):
            return True

    yaml_contents = yaml.dump(
        contents, Dumper=MyDumper, default_flow_style=False)
    with open(out_file, 'w') as out:
        out.write(yaml_contents)

    return yaml_contents


def add_meta(dataset, meta):
    for key, value in meta:
        if key in dataset:
            msg = "Meta data '%s' will override an existing value" % key
            raise RuntimeError(msg)
        dataset[key] = value


def process_user_function(dataset, user_func):
    import importlib
    path = user_func.split(".")
    mod_name = ".".join(path[:-1])
    module = importlib.import_module(mod_name)

    func_name = path[-1]
    function = getattr(module, func_name)

    function(dataset)
