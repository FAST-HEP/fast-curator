"""
Implements a curator-catalogue to CMS' DAS based on the dasgoclient command
"""
import subprocess
from .common import check_entries_uproot


_dasgoclient_prog = "dasgoclient"
_proxyinfo_prog = "voms-proxy-info"
_default_prefix = "root://cms-xrd-global.cern.ch//"


def _check_proxy():
    try:
        check_proxy = subprocess.run([_proxyinfo_prog], capture_output=True, text=True)
    except FileNotFoundError as e:
        if _proxyinfo_prog in str(e):
            msg = "%s not found. Needed to test voms proxy"
            return RuntimeError(msg % _proxyinfo_prog)
    if "Proxy not found" in check_proxy.stderr:
        msg = "No valid VOMS proxy configured.  Please run `voms-proxy-init --voms cms`"
        return RuntimeError(msg)


def _check_help():
    try:
        subprocess.run([_dasgoclient_prog, "-h"], capture_output=True)
    except FileNotFoundError as e:
        if _dasgoclient_prog in str(e):
            msg = "%s program not found, please set up necessary CMS environment"
            return RuntimeError(msg % _dasgoclient_prog)


def check_setup():
    error = _check_help()
    if error:
        raise error

    error = _check_proxy()
    if error:
        raise error
    return True


def expand_file_list(datasets, prefix=None):
    if not prefix:
        prefix = _default_prefix

    files = []
    for dataset in datasets:
        query = "-query=file dataset={}".format(dataset)
        cmd = [_dasgoclient_prog, query, "-limit", "0", "-unique"]
        das_result = subprocess.run(cmd, capture_output=True, text=True)
        files += [prefix + f for f in das_result.stdout.split("\n") if f]
    return files


def check_files(*args, **kwargs):
    return check_entries_uproot(*args, **kwargs)
