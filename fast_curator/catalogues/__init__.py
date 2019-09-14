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


def check_entries_uproot(files, tree, no_empty):
    if not no_empty:
        return files, uproot.numentries(files, tree)

    totals = uproot.numentries(files, tree, total=False)
    n_entries = sum(totals.values())
    full_list = [name for name, entries in totals.items() if entries > 0]
    return full_list, n_entries


known_expanders = dict(xrootd=XrootdExpander,
                       local=LocalGlobExpander,
                       )


def get_file_list_expander(expander):
    if expander not in known_expanders:
        msg = "Unknown file expander requested, '%s'. Valid options: %s"
        raise RuntimeError(msg % (expander, ", ".join(known_expanders.keys())))
    return known_expanders[expander]
