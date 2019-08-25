import argparse
import re
from pathlib import Path

import yaml

import backup
import batch
import link


def add_file_args(parser: argparse.ArgumentParser):
    """Add file args to command `parser`s.

    Args:
        parser (argparse.ArgumentParser): the parser to add the flags

    Returns:
        None

    """
    parser.add_argument(
        'sub_dir',
        help=(
            'The sub directory containing .gci files, '
            'excluding your save dir root'
            ),
        )
    parser.add_argument(
        '--file', '-f',
        help='One file to restore'
        )

    return


def add_batch_args(parser: argparse.ArgumentParser):
    """Add batch arg flags to command `parser`s.

    Args:
        parser (argparse.ArgumentParser): the parser to add the flags

    Returns:
        None

    """
    subparsers = parser.add_subparsers()
    file_group = subparsers.add_parser('file', help = 'file help')
    add_file_args(file_group)

    batch_group = subparsers.add_parser('batch', help = 'batch help')
    group = batch_group.add_mutually_exclusive_group(required = True)
    group.add_argument(
        '--batch', '-b',
        action='store_const',
        const=1,
        help='Batch operation on one region and one slot'
        )
    group.add_argument(
        '--batch-region', '-R',
        action='store_const',
        const=1,
        help='Batch operation on one region and both slots'
        )
    group.add_argument(
        '--batch-all', '-A',
        action='store_const',
        const=1,
        help='Batch operation on all regions and both slots'
        )

    return


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
add_file_args(parser_link)

parser_unlink = subparser.add_parser('unlink', help='unlink help')
add_batch_args(parser_unlink)

parser_backup = subparser.add_parser('backup', help='backup help')
add_batch_args(parser_backup)

parser_restore = subparser.add_parser('restore', help='restore help')
add_file_args(parser_restore)
parser_restore.add_argument(
    '--number', '-n',
    help='Backup number to restore'
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
    elif region == 'E':
        return 'EUR'
    elif region == 'J':
        return 'JAP'
    elif region == 'U':
        return 'USA'
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
    # Since `expanduser` doesn't care if '~' isn't present,
    # use it unconditionally
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
            f"""You have the following file conflicts: {" ".join(failure)}
            Please check and move/delete these files.
            """
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
            raise Exception(
                f"""{save_file} doesn't exist.
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
    else:
        region = check_region(args.region)
    base_dir = convert_check_path(conf['base_dir'])
    save_dir = convert_check_path(conf['save_dir'])
    if not (args.batch or args.batch_region or args.batch_all):
        sub_dir = convert_check_path(save_dir / args.sub_dir)
    card_slot = f'Card {args.slot}'
    card_dir = base_dir / 'GC' / region / card_slot
    max_backup = conf['max_backup']
    print(max_backup)

    try:
        if args.batch or args.batch_region or args.batch_all:
            pass
        else:
            # Maybe find a more elegant solution later.
            raise Exception
    except Exception:
        if not card_dir.exists():
            print(f'{card_dir.name} doesn\'t exist! Creating...')
            card_dir.mkdir(parents=True)

    # If sub_dir is checked instead, there is a real possibility
    # of a regular save file being deleted via `unlink`. Plus,
    # the target of unlinking is the symlinked files.
    try:
        if args.file and args.subcommand == 'unlink':
            file = check_file_exists(card_dir, Path(args.file))
        else: # elif args.file:
            file = check_file_exists(sub_dir, Path(args.file))
    except AttributeError:
        # fallback for batch operations
        file = None

    if args.subcommand == 'link':
        if check_file_conflicts(
            sub_dir, base_dir, card_slot, region, file=file
            ):
            if file:
                link.link_file(sub_dir, card_dir, file, max_backup=max_backup)
            else:
                link.link_files(sub_dir, card_dir, max_backup=max_backup)
    elif args.subcommand == 'unlink':
        if file:
            link.unlink_file(file)
        else:
            function = link.unlink_file
    elif args.subcommand == 'backup':
        if file:
            backup.backup(file, max_backup=max_backup)
        else:
            function = backup.backup
    else: # elif args.subcommand == 'restore':
        backup.restore(file, args.number)

    try:
        if args.batch:
            batch.batch(function, card_dir, max_backup = max_backup)
        elif args.batch_region:
            batch.batch_region(
                function, base_dir, region, max_backup=max_backup
                )
        else:
            batch.batch_all(
                function, base_dir, max_backup=max_backup
                )
    except AttributeError:
        pass
