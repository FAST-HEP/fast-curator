"""
Reproduce the standard glob package behaviour
"""
import glob as gl
import os
import fnmatch
import sys
if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse


__all__ = ["glob", "iglob"]


def split_url(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    path = parsed_uri.path
    return domain, path


def glob(pathname):
    # Let normal python glob try first
    try_glob = gl.glob(pathname)
    if try_glob:
        return try_glob

    # If pathname does not contain a wildcard:
    if not gl.has_magic(pathname):
        return [pathname]

    # Else try xrootd instead
    return xrootd_glob(pathname)


def xrootd_glob(pathname):
    from pyxrootd.client import FileSystem
    # Split the pathname into a directory and basename
    dirs, basename = os.path.split(pathname)

    if gl.has_magic(dirs):
        dirs = xrootd_glob(dirs)
    else:
        dirs = [dirs]

    files = []
    for dirname in dirs:
        host, path = split_url(dirname)
        query = FileSystem(host)

        if not query:
            raise RuntimeError("Cannot prepare xrootd query")

        _, dirlist = query.dirlist(path)
        for entry in dirlist["dirlist"]:
            filename = entry["name"]
            if filename in [".", ".."]:
                continue
            if not fnmatch.fnmatchcase(filename, basename):
                continue
            files.append(os.path.join(dirname, filename))

    return files


def iglob(pathname):
    for name in glob(pathname):
        yield name
