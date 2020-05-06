from .common import XrootdExpander, LocalGlobExpander
from . import cms_das as CMSDASExpander


known_expanders = dict(xrootd=XrootdExpander,
                       local=LocalGlobExpander,
                       cmsdas=CMSDASExpander,
                       )


def get_file_list_expander(expander):
    if expander not in known_expanders:
        msg = "Unknown catalogue interface requested, '%s'. Valid options: %s"
        raise RuntimeError(msg % (expander, ", ".join(known_expanders.keys())))
    result = known_expanders[expander]
    if not result.check_setup():
        msg = "Issue setting up catalogue interface: %s"
        raise RuntimeError(msg % expander)
    return result
