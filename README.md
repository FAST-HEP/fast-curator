[![pypi package](https://img.shields.io/pypi/v/fast-curator.svg)](https://pypi.org/project/fast-curator/)
[![pipeline status](https://gitlab.cern.ch/fast-hep/public/fast-curator/badges/master/pipeline.svg)](https://gitlab.cern.ch/fast-hep/public/fast-curator/commits/master)
[![coverage report](https://gitlab.cern.ch/fast-hep/public/fast-curator/badges/master/coverage.svg)](https://gitlab.cern.ch/fast-hep/public/fast-curator/commits/master)

fast-curator
=============
Create, read and write dictionary descriptions of input datasets to process.
Currently all datasets are expected to be built from ROOT Trees.

## Requirements


## Installing
```
pip install --user fast-curator[uproot]
```
Note that if you wish to handle large numbers of remote files, such as with wild-carded xrootd paths, you currently need to use the `ROOT` version of this package and not the `uproot` version.
That means changing the above command to:
```
pip install --user fast-curator[ROOT]
```

## Usage
```
# Local files:
fast_curator -o output_file_list.txt -t tree_name -d dataset_name --mc input/files/*root

# Single XROOTD files:
fast_curator -o output_file_list.txt -t tree_name -d dataset_name --mc root://my.domain.with.files://input/files/one_file.root

# XROOTD files with a glob (needs the ROOT version of fast-curator, see above)
fast_curator -o output_file_list.txt -t tree_name -d dataset_name --mc root://my.domain.with.files://input/files/*.root
```

If the command is called multiple times with the same output file (using the `-o` option), the additional files specified will be appended to the output file.

## Documentation
Is on its way...
