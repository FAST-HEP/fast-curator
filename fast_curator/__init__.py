"""Top-level package for fast-curator."""
from . import read
from . import write
from .version import __version__, version_info


__all__ = ["read", "write", "__version__", "version_info"]

__author__ = """Benjamin Krikler, and F.A.S.T"""
__email__ = 'fast-hep@cern.ch'
