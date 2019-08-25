# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.1] - 2019-08-25
### Added
- [`manager.py`](manager.py) Added `add_file_args` to reduce lines (DRY)

### Changed
- [`manager.py`](manager.py) Use subcommand groups to differentiate between files and batch operations
- [`manager.py`](manager.py) `add_batch` ➡ `add_batch_args`; consistent with `add_file_args`
- [`manager.py`](manager.py) `add_batch_args` now returns `None` to be consistent with `add_file_args`

### Fixed
- [`batch.py`](batch.py) Syntax issue
- [`manager.py`](manager.py) `AttributeError`: handling batch operations with omitted `sub_dir`

## [1.1] - 2019-08-12
### Added
- [Batch](batch.py) functionality; doesn't work with `link.link_files` or `backup.restore`
- [Unlinking](link.py) functionality
- [Backup](backup.py) and restore functionality
- Better argument handling, with subcommands

### Changed
- Command behavior slightly different, now with subcommands
- Subcommands are broken into separate files instead of one large file
- [`link.link_file`(s)](link.py) will now attempt to back up files automatically
- Improved [`README.md`](README.md)

## [1.0.1] - 2019-07-29
### Added
- Region checking for saves

### Fixed
- Typo in [`config.yaml.example`](config.yaml.example)
- Use `'GC' / region` for Dolphin saves directory

## [1.0] - 2019-07-16
### Added
- Initial version
