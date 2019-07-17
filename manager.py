import argparse
import re
from pathlib import Path

import yaml


# $ python manager.py <save sub_dir> <slot>
parser = argparse.ArgumentParser(
    description="""
        A simple save manager for Dolphin Emulator.

        Useful for multiple save files used in one game.
        """
    )
parser.add_argument(
    'sub_dir',
    help='The subdirectory containing .gci files, excluding your savedir root',
    )
parser.add_argument(
    '--slot', '-s',
    choices=['A', 'B'],
    default='A',
    help='Destination slot, A or B',
    type=str.upper
    )

gci_numbers = re.compile(r'(_[0-9]{2})?\.gci', re.I)


def convert_check_path(directory):
    directory = Path(directory).expanduser()
    if directory.exists() and directory.is_dir():
        return directory
    else:
        raise Exception(f'{directory} doesn\'t exist or isn\'t a directory')


def check_file_conflicts(sub_dir, base_dir, card_slot):
    success = []
    card_dir = base_dir / card_slot
    for file in sub_dir.glob('*.gci'):
        pattern = card_dir / gci_numbers.sub('*.gci', file.name)
        pass


if __name__ == '__main__':
    args = parser.parse_args()
    with open('config.yaml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.Loader)
    # Since `expanduser` doesn't care if '~' isn't present,
    # use it unconditionally
    base_dir = convert_check_path(conf['base_dir'])
    save_dir = convert_check_path(conf['save_dir'])
    sub_dir = convert_check_path(save_dir / args.sub_dir)
    card_slot = f'Card {args.slot}'
    
    if not check_file_conflicts(sub_dir, base_dir, card_slot):
        pass