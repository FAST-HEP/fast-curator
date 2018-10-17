from __future__ import print_function
import six
import sys

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


def from_yaml(path, defaults={}, find_associates=associate_by_ext_suffix):
    import yaml
    with open(path, 'r') as f:
        datasets_dict = yaml.load(f)
    if not datasets_dict:
        raise RuntimeError("Empty config file in '%s'" % path)
    return get_datasets(datasets_dict, defaults,
                        find_associates=associate_by_ext_suffix)


def get_datasets(datasets_dict, defaults={},
                 find_associates=associate_by_ext_suffix):
    datasets = []
    defaults.update(datasets_dict.get("defaults", {}))
    for dataset in datasets_dict["datasets"]:
        if isinstance(dataset, six.string_types):
            dataset_kwargs = _from_string(dataset, defaults)
        elif isinstance(dataset, dict):
            dataset_kwargs = _from_dict(dataset, defaults)
        else:
            raise TypeError("{} not a string or dict".format(dataset))
        datasets.append(Dataset(**dataset_kwargs))

    # Associate samples
    find_associates(datasets)

    return datasets


def _from_string(dataset, default):
    cfg = default.copy()
    cfg["name"] = dataset
    return cfg


def _from_dict(dataset, default):
    cfg = default.copy()
    cfg.update(dataset)
    if "name" not in cfg:
        raise RuntimeError(
            "Dataset provided as dict, without key-value pair for 'name'")
    return cfg
