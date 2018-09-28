from __future__ import print_function
from fast_curator.read import from_yaml
import os
from glob import glob
from collections import OrderedDict
import uproot
import logging
logger = logging.getLogger(__name__)

# uproot.tree._filename_explode('*.root')
# uproot.numentries('*.root', 'events')
# map(lambda x: (x[0], x[1], x[2]), uproot.iterate('*.root', 'events', branches='?', reportentries=True))"


def xrootd_query(path):
    if not glob.has_magic(path):
        return path

    try:
        import ROOT
    except ImportError:
        logger.error("To glob xrootd paths, we need ROOT installed (for rootpy), but it's not!!")
        raise
    from rootpy.utils.ext_glob import glob as r_glob
    return r_glob(path)


def expand_file_list(files):
    full_list = []
    for name in files:
        if name.startswith("root:"):
            expanded = xrootd_query(name)
        else:
            if not name.startswith("/"):
                name = os.path.realpath(name)
            expanded = glob(name)
        full_list += [str(exp) for exp in expanded]
    valid_files = []
    for f in full_list:
        try: 
            with uproot.open(f):
                pass
        except:
            continue
        valid_files.append(f)
    return valid_files


def prepare_file_list(files, dataset, eventtype, tree_name):
    """
    Expands all globs in the file lists and creates a dataframe similar to those from a DAS query
    """

    full_list = expand_file_list(files)
    nentries = uproot.numentries(full_list, tree_name)

    data = {}
    data["eventtype"] = eventtype
    data["name"] = dataset
    data["nevents"] = uproot.numentries(full_list, tree_name)
    data["nfiles"] = len(full_list)
    data["files"] = full_list

    return data


def write_output(dataset, out_file):
    if os.path.exists(out_file):
        contents = from_yaml(out_file)
        contents["datasets"].append(dataset)
    else:
        contents = {}
        contents["datasets"] = [dataset]

    import yaml
    with open(out_file, 'w') as out:
        yaml.dump(contents, out)

    return contents


def add_meta(dataset, meta):
    for key, value in meta:
        if key in meta:
            msg = "Meta data '%s' will override an existing value" % key
            raise RuntimeError(msg)
        dataset[key] = value


def process_args(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='*')
    parser.add_argument("-d", "--dataset", required=True, help="Which dataset to associate these files to")
    parser.add_argument("-o", "--output", default="file_list.txt", type=str, help="Name of output file list")
    parser.add_argument("--mc", dest="eventtype", action="store_const", const="mc", default=None,
                        help="Specify if this dataset contains simulated data")
    parser.add_argument("--data", dest="eventtype", action="store_const", const="data", 
                        help="Specify if this dataset contains real data")
    parser.add_argument("-t", "--tree-name", default="Events", type=str,
                        help="Provide the name of the tree in the input files to calculate number of events, etc")
    def split_meta(arg):
        if "=" not in arg:
            msg = "option not of the form 'key=value'"
            raise argparse.ArgumentTypeError(msg)
        split = arg.split("=", 2)
        return split

    parser.add_argument("-m", "--meta", action="append", type=split_meta,
                        help="Add other metadata (eg cross-section, run era) for this dataset." 
                             + "  Must take the form of 'key=value' ")
    args = parser.parse_args()
    return args


def main(args=None):
    args = process_args(args)
    dataset = prepare_file_list(files=args.files, dataset=args.dataset,
                                eventtype=args.eventtype, tree_name=args.tree_name)
    add_meta(dataset, args.meta)

    content = write_output(dataset, args.output)
    print(content)

if __name__ == "__main__":
    main()
