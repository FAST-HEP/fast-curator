from __future__ import print_function
from . import write
from . import read


def process_args_write(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='*')
    parser.add_argument("-d", "--dataset", required=True,
                        help="Which dataset to associate these files to")
    parser.add_argument("-o", "--output", default="file_list.txt",
                        type=str, help="Name of output file list")
    parser.add_argument("--mc", dest="eventtype", action="store_const", const="mc", default=None,
                        help="Specify if this dataset contains simulated data")
    parser.add_argument("--data", dest="eventtype", action="store_const", const="data",
                        help="Specify if this dataset contains real data")
    parser.add_argument("-t", "--tree-name", default="Events", type=str,
                        help="Provide the name of the tree in the input files to calculate number of events, etc")
    parser.add_argument("-u", "--user", default=[], type=str, action="append",
                        help="Add a user function to extend the dataset dictionary,"
                             " eg. my_package.my_module.some_function")

    def split_meta(arg):
        if "=" not in arg:
            msg = "option not of the form 'key=value'"
            raise argparse.ArgumentTypeError(msg)
        split = arg.split("=", 2)
        return split

    parser.add_argument("-m", "--meta", action="append", type=split_meta, default=[],
                        help="Add other metadata (eg cross-section, run era) for this dataset."
                             + "  Must take the form of 'key=value' ")
    return parser


def main_write(args=None):
    parser = process_args_write(args)
    args = parser.parse_args()

    dataset = write.prepare_file_list(files=args.files, dataset=args.dataset,
                                      eventtype=args.eventtype, tree_name=args.tree_name)
    write.add_meta(dataset, args.meta)
    for user_func in args.user:
        write.process_user_function(dataset, user_func)

    write.write_yaml(dataset, args.output)


def process_args_check(args=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs='*')
    parser.add_argument("-o", "--output", default=None,
                        type=str, help="Name of output file list to expand things to")
    parser.add_argument("-f", "--fields", default="nfiles",
                        type=str, help="Comma-separated list of fields to dump for each dataset ")
    args = parser.parse_args()

    args.fields = args.fields.split(",")
    return args


def main_check(args=None):
    args = process_args_check(args)

    datasets = []
    for infile in args.files:
        datasets += read.from_yaml(infile)

    for dataset in datasets:
        if len(dataset.files) != dataset.nfiles:
            msg = "{d.name}: corrupted dataset: bad nfiles value, should be: {len}, got: {d.nfiles}"
            print(msg.format(d=dataset, len=len(dataset.files)))
            continue
        print("==", dataset.name, "==")
        for field in args.fields:
            msg = "   %(field)s = {d.%(field)s}" % dict(field=field)
            print(msg.format(d=dataset))
    print("Total number of datasets:", len(datasets))

    if args.output:
        datasets = write.prepare_contents(datasets)
        write.write_yaml(datasets, args.output, append=False)
