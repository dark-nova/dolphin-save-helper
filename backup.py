import shutil
from pathlib import Path


def copy(src: pathlib.Path, dest: pathlib.Path):
    """Copy backup from `src` to `dest`.

    Args:
        src (pathlib.Path): the source to copy from
        dest (pathlib.Path): the destination to copy to

    Returns:
        bool: True if successful

    """
    shutil.copy(str(src), str(dest))
    return True


def backup(file: pathlib.Path, max_backup: int = 1):
    """Backs up a file, with `max_backup` indicating
    how many circular copies should be kept.

    Always attempts to resolve `file`, even if it isn't
    a symlink.

    Can be used with batch.

    Backups are "{file.name}-{backup_number}".

    Args:
        file (pathlib.Path): the file to attempt to back up
        max_backup (int, optional): maximum circular backup count;
            defaults to 1; should always be >= 1

    Returns:
        bool: True if successful

    """
    resolved = file.resolve()
    backup_dir = resolved.parent / 'backups'
    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)

    if max_backup < 1:
        max_backup = 1

    # Since the file you are backing up should be newer,
    # let's use it for the temporary `oldest_time`
    oldest_time = file.stat().st_mtime
    oldest = backup_dir / f'{file.name}-1'

    for i in range(max_backup):
        current = backup_dir / f'{file.name}-{i}'
        if not current.exists():
            return copy(resolved, current)
        elif current.stat().st_mtime < oldest_time:
            oldest_time = current.stat().st_mtime
            oldest = current

    return copy(resolved, oldest)    
