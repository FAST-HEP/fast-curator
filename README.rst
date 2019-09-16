[![pypi package](https://img.shields.io/pypi/v/fast-curator.svg)](https://pypi.org/project/fast-curator/)
[![pipeline status](https://gitlab.cern.ch/fast-hep/public/fast-curator/badges/master/pipeline.svg)](https://gitlab.cern.ch/fast-hep/public/fast-curator/commits/master)
[![coverage report](https://gitlab.cern.ch/fast-hep/public/fast-curator/badges/master/coverage.svg)](https://gitlab.cern.ch/fast-hep/public/fast-curator/commits/master)

fast-curator
=============
Create, read and write dictionary descriptions of input datasets to process.
Currently all datasets are expected to be built from sets of ROOT Trees.

## Requirements


## Installing
```
pip install --user fast-curator
```

## Usage
```
# Local files:
fast_curator -o output_file_list.txt -t tree_name -d dataset_name --mc input/files/*root

# Single XROOTD files:
fast_curator -o output_file_list.txt --mc root://my.domain.with.files://input/files/one_file.root

# XROOTD files with several globs
fast_curator -o output_file_list.txt --mc root://my.domain.with.files://inp*/files/*.root
```

Notes:
1. If the command is called multiple times with the same output file (using the `-o` option), the additional files specified will be appended to the output file.
2. Arbitrary meta-data (such as cross-section, data quality, generator precision, etc) can be added to each dataset with
   the `-m` option.

For more guidance try the built-in help:
```
fast_curator --help
```

## Reading dataset files back
```
import fast_curator
datasets = fast_curator.read.from_yaml("my_dataset_file.yml")
```
Will return a list of datasets with the `default` section applied to each dataset.

## Further Documentation
Is on its way...
