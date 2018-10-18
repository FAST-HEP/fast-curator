from . import write


def process_args(args=None):
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

    def split_meta(arg):
        if "=" not in arg:
            msg = "option not of the form 'key=value'"
            raise argparse.ArgumentTypeError(msg)
        split = arg.split("=", 2)
        return split

    parser.add_argument("-m", "--meta", action="append", type=split_meta, default=[],
                        help="Add other metadata (eg cross-section, run era) for this dataset."
                             + "  Must take the form of 'key=value' ")
    args = parser.parse_args()
    return args


def main(args=None):
    args = process_args(args)
    dataset = write.prepare_file_list(files=args.files, dataset=args.dataset,
                                      eventtype=args.eventtype, tree_name=args.tree_name)
    write.add_meta(dataset, args.meta)

    write.write_yaml(dataset, args.output)


if __name__ == "__main__":
    main()
