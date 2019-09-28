import uproot


class XrootdExpander():
    """
    Expand wild-carded file paths, including with xrootd-served files
    """
    from .. import xrootd_glob

    @staticmethod
    def expand_file_list(files):
        full_list = []
        for name in files:
            expanded = XrootdExpander.xrootd_glob.glob(name)
            full_list += map(str, expanded)
        return full_list

    @staticmethod
    def check_entries(*args, **kwargs):
        return check_entries_uproot(*args, **kwargs)


class LocalGlobExpander():
    """
    Expand wild-carded file paths on the local file system
    """
    import glob

    @staticmethod
    def expand_file_list(files):
        full_list = []
        for name in files:
            expanded = LocalGlobExpander.glob.glob(name)
            full_list += map(str, expanded)
        return full_list

    @staticmethod
    def check_entries(*args, **kwargs):
        return check_entries_uproot(*args, **kwargs)


def check_entries_uproot(files, tree, no_empty, confirm_tree=True):
    no_empty = no_empty or confirm_tree
    if not no_empty:
        return files, uproot.numentries(files, tree)

    totals = uproot.numentries(files, tree, total=False)
    n_entries = 0
    full_list = []
    missing_trees = []
    for name, entries in totals.items():
        n_entries += entries
        if not no_empty or entries > 0:
            full_list.append(name)
        if confirm_tree and entries == 0:
            if tree not in uproot.open(name):
                missing_trees.append(name)
    if missing_trees:
        msg = "Tree '%s' wasn't found for %d file(s): %s"
        msg = msg % (tree, len(missing_trees), ", ".join(missing_trees))
        raise RuntimeError(msg)

    return full_list, n_entries


known_expanders = dict(xrootd=XrootdExpander,
                       local=LocalGlobExpander,
                       )


def get_file_list_expander(expander):
    if expander not in known_expanders:
        msg = "Unknown file expander requested, '%s'. Valid options: %s"
        raise RuntimeError(msg % (expander, ", ".join(known_expanders.keys())))
    return known_expanders[expander]
