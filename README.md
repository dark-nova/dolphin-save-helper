# Dolphin Save Helper

## Overview

I made this project in response to Dolphin Emulator's somewhat rigid memory card management. I have several `.gci` files of same games, as a result of dumping my GameCube memory cards. I also wanted to manually pick which set of files to use. As a result, I wrote up this project to help manage the files, without extensive use of the command line.

## Usage

### Main
```
$ python manager.py -h
usage: manager.py [-h] [--slot {A,B}] [--region {E,EUR,J,JAP,U,USA}]
                  {link,unlink,backup,restore} ...

A simple save manager for Dolphin Emulator. Useful for multiple save files
used in one game.

positional arguments:
  {link,unlink,backup,restore}
                        subcommand help
    link                link help
    unlink              unlink help
    backup              backup help
    restore             restore help

optional arguments:
  -h, --help            show this help message and exit
  --slot {A,B}, -s {A,B}
                        Destination slot, A or B
  --region {E,EUR,J,JAP,U,USA}, -r {E,EUR,J,JAP,U,USA}
                        Region, by first letter or three letters only
```

### [Link](link.py)
```
$ python manager.py link -h
usage: manager.py link [-h] [--file FILE] sub_dir

positional arguments:
  sub_dir               The sub directory containing .gci files, excluding
                        your save dir root

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  One file to link
```

⚠ Note that using the `link` subcommand will also automatically backup the file to link.

### [Unlink](link.py)
```
$ python manager.py unlink -h
usage: manager.py unlink [-h] {file,batch} ...

positional arguments:
  {file,batch}
    file        file help
    batch       batch help

optional arguments:
  -h, --help    show this help message and exit
```

⚠ The two blocks below also apply for **Backup**.

#### File-based operations
```
$ python manager.py unlink file -h
usage: manager.py unlink file [-h] [--file FILE] sub_dir

positional arguments:
  sub_dir               The sub directory containing .gci files, excluding
                        your save dir root

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  One file to restore
```

#### Batch operations
```
$ python manager.py unlink batch -h
usage: manager.py unlink batch [-h] (--batch | --batch-region | --batch-all)

optional arguments:
  -h, --help          show this help message and exit
  --batch, -b         Batch operation on one region and one slot
  --batch-region, -R  Batch operation on one region and both slots
  --batch-all, -A     Batch operation on all regions and both slots
```

### [Backup](backup.py)
```
$ python manager.py backup -h
usage: manager.py backup [-h] {file,batch} ...

positional arguments:
  {file,batch}
    file        file help
    batch       batch help

optional arguments:
  -h, --help    show this help message and exit
```

⚠ See above in the **Unlink** section for *file* and *batch operations*.

### [Restore](backup.py)
```
$ python manager.py restore -h
usage: manager.py restore [-h] [--file FILE] [--number NUMBER] sub_dir

positional arguments:
  sub_dir               The sub directory containing .gci files, excluding
                        your save dir root

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  One file to restore
  --number NUMBER, -n NUMBER
                        Backup number to restore
```

⚠ Note that although this program attempts to manipulate files in a safe manner (using symlinks, for example), `restore` is a destructive procedure that overwrites the save file with the backup.

## [Config](config.yaml.example)
Examine the file:

e.g. Your `save_dir` is `~/GCN/saves` (equivalent to `/home/user/GCN/saves`). If your specific game saves is in `game1` in the parent `save_dir` (full path: `/home/user/GCN/saves/game1`), then use `game1` in the command as `sub_dir`.

You should configure `region` as defined in the file. You can override this in the command using `-r` or `--region` followed by the region, e.g. `-r USA`.

You can change `max_backup` to a number of your choice. If it's invalid, the program will ignore the value and use a default of 1.

## Disclaimer

This project is not affiliated with or endorsed by Dolphin Emulator or Nintendo. See [LICENSE](LICENSE) for additional detail.
