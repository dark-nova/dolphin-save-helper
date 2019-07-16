import argparse
from pathlib import Path

import yaml


# $ python manager.py <save subdir> <slot>
parser = argparse.ArgumentParser(
    description="""
        A simple save manager for Dolphin Emulator
        """
    )
parser.add_argument(
    'subdir',
    help='The subdirectory containing .gci files, excluding your savedir root',
    )
parser.add_argument(
    '--slot', '-s',
    choices=['A', 'B'],
    default='A',
    help='Destination slot, A or B',
    type=str.upper
    )
