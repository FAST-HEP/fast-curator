import six
import sys
import os

if sys.version_info[0] >= 3.3:
    from types import SimpleNamespace as Dataset
else:
    from argparse import Namespace as Dataset


def associate_by_ext_suffix(datasets):
    has_ext = []
    has_no_ext = []
    for dataset in datasets:
        out_list = has_ext if "_ext" in dataset.name else has_no_ext
        out_list.append(dataset)

    for dataset in has_no_ext:
        associates = [d for d in has_ext if d.name.startswith(dataset.name)]
        associates.append(dataset)
        names = [a.name for a in associates]
        for index in range(len(associates)):
            associates[index].associates = names[:index]
            associates[index].associates += names[index + 1:]


def _load_yaml(path):
    import yaml
    with open(path, 'r') as f:
        datasets_dict = yaml.safe_load(f)
    if not datasets_dict:
        raise RuntimeError("Empty config file in '%s'" % path)
    return datasets_dict


def from_yaml(path, defaults={}, find_associates=associate_by_ext_suffix,
              selected_prefix=None, expand_prefix=True):
    datasets_dict = _load_yaml(path)
    this_dir = os.path.dirname(os.path.abspath(path))
    return get_datasets(datasets_dict, defaults, this_dir=this_dir,
                        selected_prefix=selected_prefix,
                        expand_prefix=expand_prefix,
                        find_associates=associate_by_ext_suffix)


def get_datasets(datasets_dict, defaults={},
                 find_associates=associate_by_ext_suffix, already_imported=None,
                 this_dir=None, selected_prefix=None, expand_prefix=True):
    datasets = []
    defaults.update(datasets_dict.get("defaults", {}))
    if "import" not in datasets_dict and "datasets" not in datasets_dict:
        raise RuntimeError("Neither 'datasets' nor 'import' were specified in config")

    if already_imported is None:
        already_imported = set()
    for import_file in datasets_dict.get("import", []):
        if this_dir:
            import_file = import_file.format(this_dir=this_dir)
        if import_file in already_imported:
            continue
        already_imported.add(import_file)
        contents = _load_yaml(import_file)
        datasets += get_datasets(contents, defaults=defaults.copy(), this_dir=os.path.dirname(import_file),
                                 find_associates=find_associates, already_imported=already_imported)
    for dataset in datasets_dict.get("datasets", []):
        if isinstance(dataset, six.string_types):
            cfg = _from_string(dataset, defaults)
        elif isinstance(dataset, dict):
            cfg = _from_dict(dataset, defaults, selected_prefix)
        else:
            raise TypeError("{} not a string or dict".format(dataset))
        if expand_prefix:
            prefix = cfg.get("prefix", None)
            files = apply_prefix(prefix, cfg["files"], selected_prefix, cfg["name"])
            cfg["files"] = files
        datasets.append(Dataset(**cfg))

    # Associate samples
    find_associates(datasets)

    return datasets


def _from_string(dataset, default):
    cfg = default.copy()
    cfg["name"] = dataset
    return cfg


def _from_dict(dataset, default, selected_prefix=None):
    cfg = default.copy()
    cfg.update(dataset)
    if "name" not in cfg:
        raise RuntimeError(
            "Dataset provided as dict, without key-value pair for 'name'")
    return cfg


def apply_prefix(prefix, files, selected_prefix, dataset):
    if not prefix:
        return files

    if isinstance(prefix, list):
        if not all((isinstance(p, dict) and len(p) == 1 for p in prefix)):
            raise ValueError("'prefix' is a list, but not all elements are single-length dicts")
        prefix = [tuple(p.items())[0] for p in prefix]
        if selected_prefix:
            matched = [v for p, v in prefix if p == selected_prefix]
            if len(matched) > 1:
                msg = "Prefix '%s' is defined %d times, not sure which to use"
                raise ValueError(msg % (selected_prefix, len(matched)))
            if not matched:
                msg = "Prefix '%s' is not defined for dataset '%s'"
                raise ValueError(msg % (selected_prefix, dataset))
            prefix = matched[0]
        else:
            prefix = prefix[0][1]
    elif not isinstance(prefix, six.string_types):
        msg = "'prefix' for dataset '%s' is type '%s'. Need a string or a list of single-length dicts"
        raise ValueError(msg % (dataset, type(prefix)))

    return [f.format(prefix=prefix) for f in files]
