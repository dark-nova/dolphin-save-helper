from pathlib import Path

import backup


def link_files(sub_dir: str, base_dir: str, card_slot: str, region: str,
    max_backup: int = 1):
    """Link files from `sub_dir` into `base_dir` / `card_slot`.
    If `card_slot` doesn't exist, create it.

    Due to requiring `sub_dir` and `base_dir` for processing,
    `link_files` cannot be used in batch.

    Will automatically call `backup.backup()` per file.

    Args:
        sub_dir (str): the sub dir containing your saves elsewhere
        base_dir (str): the base dir created and used by Dolphin Emulator
        card_slot (str): either 'Card A' or 'Card B'
        region (str): 'EUR', 'JAP', 'USA'
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True

    """
    card_dir = base_dir / 'GC' / region / card_slot
    if not card_dir.exists():
        print(f'{card_dir.name} doesn\'t exist! Creating...')
        card_dir.mkdir(parents=True)

    for file in sub_dir.glob(GCI_GLOB):
        current = card_dir / file.name
        current.symlink_to(file)
        print(f'Linked {file.name}!')
        backup.backup(file, max_backup)

    return True


def unlink_file(file: pathlib.Path):
    """Unlink one file, given a `file`.

    Compare with `link_files` (plural); to be used with batch.

    Args:
        file (pathlib.Path): the file to attempt to delete

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
