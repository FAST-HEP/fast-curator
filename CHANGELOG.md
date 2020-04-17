# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]
### Added
### Changed
### Removed

## [0.6.0] - 2020-04-17
### Changed
- Use Xrootd's implementation of xrootd_glob not our own version

## [0.5.0] - 2020-01-27
### Added
- Support for handling files which can't be opened PR #36 [@seriksen](https://github.com/seriksen)

## [0.4.1] - 2019-10-06
### Changed
- Save tree_name as single string if only one tree included, PR #30

## [0.4.0] - 2019-10-06
### Added
- Support for handling mulitple input trees in each file, PR #28
- Support for file prefix selection, PR #29

## [0.3.2] - 2019-09-29
### Changed
- Fix setup.py to include sub-directories in package, PR #27.

## [0.3.1] - 2019-09-28
### Changed
- Automate pypi deployment

## [0.3.0] - 2019-09-28
### Added
- Generic interface for file path expansion, PR #20. [@benkrikler](https://github.com/benkrikler)
- Add option to ignore empty files, issue #5. [@benkrikler](https://github.com/benkrikler)
- Report files with missing trees, issue #16, PR #24. [@benkrikler](https://github.com/benkrikler)

### Changed
- Switch README to restructured text and update setup.py, PR 23.
- Restructure package version numbering, PR #19. [@benkrikler](https://github.com/benkrikler)
- Unit tests to improve test coverage and minor fixes, PR #25. [@benkrikler](https://github.com/benkrikler)

## [0.2.2] - 2019-07-28
### Added
- Added this changelog [@benkrikler](https://github.com/benkrikler)

### Changed
- Make sure the `args` parameter is passed through to the main functions in `__main__.py`, issue #9. [@benkrikler](https://github.com/benkrikler)
- Switch to pyyaml `safe_load` for better security, issue #8. [@benkrikler](https://github.com/benkrikler)
- Expand an input file's path to an absolute path for `this_dir` to be meaningful, issue #7. [@benkrikler](https://github.com/benkrikler)

## [0.2.1] - 2019-03-01
