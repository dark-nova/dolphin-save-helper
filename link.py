from pathlib import Path

import backup


def link_file(sub_dir: Path, card_dir: Path, file: Path, max_backup: int = 1):
    """Link one file from `sub_dir` into `base_dir` / `card_slot`.
    If `card_slot` doesn't exist, create it.

    Due to requiring `sub_dir` and `base_dir` for processing,
    `link_file` cannot be used in batch.

    Will automatically call `backup.backup()` per file.

    Args:
        sub_dir (str): the sub dir containing your saves elsewhere
        card_dir (Path): base_dir / 'GC' / region / card_slot
        file (Path): the file
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True if successful

    """
    linked = card_dir / file.name
    linked.symlink_to(save_file)
    print(f'Linked {save_file.name}!')
    backup.backup(save_file, max_backup=max_backup)

    return True


def link_files(sub_dir: Path, card_dir: Path, max_backup: int = 1):
    """Link files from `sub_dir` into `base_dir` / `card_slot`.

    Calls `link_file` - check docstring for more information.

    Args:
        sub_dir (Path): the sub dir containing your saves elsewhere
        card_dir (Path): base_dir / 'GC' / region / card_slot
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True

    Raises:
        Exception: see `link_file`

    """
    for file in sub_dir.glob(GCI_GLOB):
        link_file(sub_dir, card_dir, file, max_backup)

    return True


def unlink_file(file: Path):
    """Unlink one file, given a `file`.

    Compare with `link_files` (plural); can be used with batch.

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
