# Dolphin Save Helper

## Overview

I made this project in response to Dolphin Emulator's somewhat rigid memory card management. I have several `.gci` files of same games, as a result of dumping my GameCube memory cards. I also wanted to manually pick which set of files to use. As a result, I wrote up this project to help manage the files, without extensive use of the command line.

## Usage

```
python manager.py [-h] [--slot {A,B}] sub_dir

A simple save manager for Dolphin Emulator. Useful for multiple save files
used in one game.

positional arguments:
  sub_dir               The sub directory containing .gci files, excluding
                        your save dir root

optional arguments:
  -h, --help            show this help message and exit
  --slot {A,B}, -s {A,B}
                        Destination slot, A or B

```

More specifically, if your `save_dir` in [`config.yaml`](config.yaml.example) is e.g. `/home/user/GCN/saves` (or `~/GCN/saves`) and your `sub_dir` is `game1` (full path: `/home/user/GCN/saves/game1`), you should only use `game1` as the argument.

Set slot if that is important.
