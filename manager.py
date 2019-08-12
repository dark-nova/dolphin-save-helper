import argparse
import re
from pathlib import Path

import yaml

import backup
import batch
import link


parser = argparse.ArgumentParser(
    description="""
        A simple save manager for Dolphin Emulator.

        Useful for multiple save files used in one game.
        """
    )
parser.add_argument(
    '--slot', '-s',
    choices=['A', 'B'],
    default='A',
    help='Destination slot, A or B',
    type=str.upper
    )
parser.add_argument(
    '--region', '-r',
    choices=['E', 'EUR', 'J', 'JAP', 'U', 'USA'],
    help='Region, by first letter or three letters only',
    type=str.upper
    )

subparser = parser.add_subparsers(
    help='subcommand help',
    required=True,
    dest='subcommand'
    )

parser_link = subparser.add_parser('link', help='link help')
parser_link.add_argument(
    'sub_dir',
    help=(
        'The sub directory containing .gci files, '
        'excluding your save dir root'
        ),
    )
parser_link.add_argument(
    '--file',
    help='One file to link'
    )

parser_unlink = subparser.add_parser('unlink', help='unlink help')

parser_backup = subparser.add_parser('backup', help='backup help')

parser_restore = subparser.add_parser('restore', help='restore help')
parser_restore.add_argument(
    'sub_dir',
    help=(
        'The sub directory containing .gci files, '
        'excluding your save dir root'
        ),
    )
parser_restore.add_argument(
    '--file',
    help='One file to restore'
    )

def add_batch(parser: argparse.ArgumentParser):
    """Add batch flags to command `parser`s.

    Args:
        parser (argparse.ArgumentParser): the parser to add the flags

    Returns:
        bool: True

    """
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--file',
        help='One file, instead of batch'
        )
    group.add_argument(
        '--batch',
        action='store_const',
        const=1,
        help='Batch operation on one region and one slot'
        )
    group.add_argument(
        '--batch-region',
        action='store_const',
        const=1,
        help='Batch operation on one region and both slots'
        )
    group.add_argument(
        '--batch-all',
        action='store_const',
        const=1,
        help='Batch operation on all regions and both slots'
        )

    return True


add_batch(parser_unlink)
add_batch(parser_backup)


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
    sub_dir: Path, base_dir: Path, card_slot: str, region: str,
    file: Path = None
    ):
    """Checks for file conflicts. If conflicts exist, abort script.
    Otherwise, remove existing, valid symlinks.

    Conflicting files:
    - regular files with same or similar name
    - symlinks pointing to the same files as the ones in sub_dir

    Args:
        sub_dir (Path): the sub dir containing your saves elsewhere
        base_dir (Path): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'
        file (Path, optional): single file to check; defaults to None

    Returns:
        bool: True, if files exist in `sub_dir` but not in
        `base_dir` `card_slot`

    Raises:
        Exception: if unsuccessful

    """
    non_empty = False
    failure = []
    card_dir = base_dir / 'GC' / region / card_slot
    if file:
        files = [file]
    else:
        files = sub_dir.glob(GCI_GLOB)
    for f in files:
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


def check_file_exists(sub_dir: Path, file: Path):
    """Check if the supplied `file` arg exists.

    Args:
        sub_dir (Path): the fully qualified subdirectory
        file (Path): the file to check

    Returns:
        Path: if valid, the file

    Raises:
        Exception: if save file doesn't exist or is in the wrong place

    """
    if file.resolve().parent != sub_dir:
        raise Exception(f'{file} isn\'t in {sub_dir}')
    if file.exists():
        return file
    else:
        save_file = sub_dir / file
        if not save_file.exists():
            raise Exception(f"""
                {save_file} doesn\'t exist.
                Please check the filename and/or location.
                """
                )

        return save_file


if __name__ == '__main__':
    args = parser.parse_args()
    with open('config.yaml', 'r') as f:
        conf = yaml.load(f, Loader=yaml.Loader)
    if not args.region:
        region = check_region(conf['region'])
    elif args.region == 'E':
        region = 'EUR'
    elif args.region == 'J':
        region = 'JAP'
    elif args.region == 'U':
        region = 'USA'
    else:
        region = args.region
    # Since `expanduser` doesn't care if '~' isn't present,
    # use it unconditionally
    base_dir = convert_check_path(conf['base_dir'])
    save_dir = convert_check_path(conf['save_dir'])
    sub_dir = convert_check_path(save_dir / args.sub_dir)
    card_slot = f'Card {args.slot}'

    if args.file:
        file = check_file_exists(sub_dir, Path(args.file))
    else:
        file = None

    if args.subcommand == 'link':
        if check_file_conflicts(
            sub_dir, base_dir, card_slot, region, file=file
            ):
            link.link_files(sub_dir, base_dir, card_slot, region)
