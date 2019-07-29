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
    help=(
        'The sub directory containing .gci files, '
        'excluding your save dir root'
        ),
    )
parser.add_argument(
    '--slot', '-s',
    choices=['A', 'B'],
    default='A',
    help='Destination slot, A or B',
    type=str.upper
    )

GCI_NUMBERS = re.compile(r'(_[0-9]{2})?\.gci', re.I)

GCI_GLOB = '*.gci'


def check_region(region: str):
    """Checks and validates region from config.
    Regions can only be 'EUR', 'JAP', or 'USA', as defined by
    Dolphin Emulator.

    Args:
        region (str): the geographic region of the game's saves

    Returns:
        str: region, if valid

    Raises:
        Exception: if the config region is invalid

    """
    if region == 'EUR' or region == 'JAP' or region == 'USA':
        return region
    else:
        raise Exception(f'{region} is an invalid region!')


def convert_check_path(directory: str):
    """Expands tilde if present (convert). Checks the resulting path
    for existence.

    Args:
        directory (str): the `save_dir` arg; the user's directory to use

    Returns:
        str: the directory, full path

    Raises:
        Exception: if the directory doesn't exist or isn't a directory

    """
    directory = Path(directory).expanduser()
    if directory.exists() and directory.is_dir():
        return directory
    else:
        raise Exception(f'{directory} doesn\'t exist or isn\'t a directory')


def check_file_conflicts(
    sub_dir: str, base_dir: str, card_slot: str, region: str
    ):
    """Checks for file conflicts. If conflicts exist, abort script.
    Otherwise, remove existing, valid symlinks.

    Conflicting files:
    - regular files with same or similar name
    - symlinks pointing to the same files as the ones in sub_dir

    Args:
        sub_dir (str): the sub dir containing your saves elsewhere
        base_dir (str): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'

    Returns:
        bool: True, if files exist in `sub_dir` but not in
        `base_dir` `card_slot`

    Raises:
        Exception: if unsuccessful

    """
    non_empty = False
    failure = []
    card_dir = base_dir / 'GC' / region / card_slot
    for file in sub_dir.glob(GCI_GLOB):
        non_empty = True
        for g in card_dir.glob(GCI_NUMBERS.sub(GCI_GLOB, file.name)):
            if g.is_symlink() and g.name != file.name:
                g.unlink()
            else:
                failure.append(g.name)

    if non_empty and not failure:
        return True
    elif not non_empty:
        raise Exception(f'{sub_dir} doesn\'t have any .gci files')
    else:
        raise Exception(
            f'You have the following file conflicts: {" ".join(failure)}'
            )


def link_files(sub_dir: str, base_dir: str, card_slot: str, region: str):
    """Link files from `sub_dir` into `base_dir` / `card_slot`.
    If `card_slot` doesn't exist, create it.

    Args:
        sub_dir (str): the sub dir containing your saves elsewhere
        base_dir (str): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'

    Returns:
        bool: True

    """
    card_dir = base_dir / 'GC' / region / card_slot
    if not card_dir.exists():
        card_dir.mkdir(parents=True)

    for file in sub_dir.glob(GCI_GLOB):
        current = card_dir / file.name
        current.symlink_to(file)
        print(f'Linked {file.name}!')

    return True


if __name__ == '__main__':
    args = parser.parse_args()
    with open('config.yaml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.Loader)
    # Since `expanduser` doesn't care if '~' isn't present,
    # use it unconditionally
    region = check_region(conf['region'])
    base_dir = convert_check_path(conf['base_dir'])
    save_dir = convert_check_path(conf['save_dir'])
    sub_dir = convert_check_path(save_dir / args.sub_dir)
    card_slot = f'Card {args.slot}'
    
    if check_file_conflicts(sub_dir, base_dir, card_slot, region):
        link_files(sub_dir, base_dir, card_slot, region)
