from pathlib import Path

import backup


def link_file(sub_dir: Path, base_dir: Path, card_slot: str, region: str,
    file: Path, max_backup: int = 1):
    """Link one file from `sub_dir` into `base_dir` / `card_slot`.
    If `card_slot` doesn't exist, create it.

    Due to requiring `sub_dir` and `base_dir` for processing,
    `link_file` cannot be used in batch.

    Will automatically call `backup.backup()` per file.

    Args:
        sub_dir (str): the sub dir containing your saves elsewhere
        base_dir (str): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'
        file (Path): the file
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True if successful

    Raises:
        Exception: if save file doesn't exist or is in the wrong place

    """
    card_dir = base_dir / 'GC' / region / card_slot
    if not card_dir.exists():
        print(f'{card_dir.name} doesn\'t exist! Creating...')
        card_dir.mkdir(parents=True)

    if file.resolve().parent != sub_dir:
        raise Exception(f'{file} isn\'t in {sub_dir}')
    if file.exists():
        save_file = file
    else:
        save_file = sub_dir / file
        if not save_file.exists():
            raise Exception(f"""
                {save_file} doesn\'t exist.
                Please check the filename and/or location.
                """
                )

    linked = card_dir / file.name
    linked.symlink_to(save_file)
    print(f'Linked {save_file.name}!')
    backup.backup(save_file, max_backup=max_backup)

    return True


def link_files(sub_dir: Path, base_dir: Path, card_slot: str, region: str,
    max_backup: int = 1):
    """Link files from `sub_dir` into `base_dir` / `card_slot`.

    Calls `link_file` - check docstring for more information.

    Args:
        sub_dir (Path): the sub dir containing your saves elsewhere
        base_dir (Path): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True

    Raises:
        Exception: see `link_file`

    """
    for file in sub_dir.glob(GCI_GLOB):
        link_file(sub_dir, base_dir, card_slot, region, file, max_backup)

    return True


def unlink_file(file: Path):
    """Unlink one file, given a `file`.

    Compare with `link_files` (plural); to be used with batch.

    Args:
        file (Path): the file to attempt to delete

    Returns:
        bool: True if successful; False otherwise

    """
    try:
        file.unlink()
        print(f'Successfully unlinked {file.name}!')
        return True
    except:
        print(f'Could not unlink {file.name}.')
        return False
