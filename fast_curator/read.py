from __future__ import print_function
import os
import six
import logging
import sys

if sys.version_info[0] >= 3.3:
    from types import SimpleNamespace as Dataset
else:
    from argparse import Namespace as Dataset


def from_yaml(path, defaults={}):
    import yaml
    with open(path, 'r') as f:
        datasets_dict = yaml.load(f)
    if not datasets_dict:
        raise RuntimeError("Empty config file in '%s'" % path)
    return get_datasets(datasets_dict, defaults)


def _associate_by_ext_suffix(datasets):
    not_extensions = [dataset for dataset in datasets
                      if not dataset.name.endswith("_ext")]

    for not_extension in not_extensions:
        associated_datasets = [dataset
                               for dataset in datasets
                               if not_extension.name in dataset.name]
        for dataset in associated_datasets:
            dataset.associates = associated_datasets


def get_datasets(datasets_dict, defaults={}, 
                 find_associates=_associate_by_ext_suffix):
    datasets = []
    defaults.update(datasets_dict.get("default", {}))
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
        raise RuntimeError("Dataset provided as dict, without key-value pair for 'name'")
    return cfg
