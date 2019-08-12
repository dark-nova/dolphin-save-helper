from pathlib import Path


def batch(action, card_dir: Path):
    """Performs an `action` repeatedly across a given `region` and
    `card_slot`.

    Before using this function, ensure all parameters are valid.

    Args:
        action (function): the function to run in batch
        card_dir (Path): base_dir / 'GC' / region / card_slot

    Returns:
        bool: True

    Raises:
        Exception: if `action` fails at any given time, or
        regular files exist

    """
    failure = []
    for file in card_dir.glob('*.gci'):
        if file.is_symlink():
            if not action(file):
                failure.append(file.name)
        else:
            failure.append(file.name)

    if failure:
        raise Exception(
            f"""You have The following file conflicts:
            {' '.join(failure)}"""
            )
    else:
        return True


def batch_region(action, base_dir: str, region: str):
    """Performs an `action` repeatedly across a given `region`.
    Both card slots 'A' and 'B' are checked.

    Before using this function, ensure all parameters are valid.

    Args:
        action (function): the function to run in batch
        base_dir (str): the base dir created and used by Dolphin Emulator
        region (str): 'EUR', 'JAP', 'USA'

    Returns:
        bool: True

    Raises:
        Exception: if `action` fails at any given time, or
        regular files exist

    """
    for slot in ['A', 'B']:
        card_dir = Path(base_dir) / 'GC' / region / f'Card {slot}'
        batch(action, card_dir)

    return True


def batch_all(action, base_dir: str):
    """Performs an `action` on all regions and card slots.

    Before using this function, ensure all parameters are valid.

    Args:
        action (function): the function to run in batch
        base_dir (str): the base dir created and used by Dolphin Emulator

    Returns:
        bool: True

    Raises:
        Exception: if `action` fails at any given time, or
        regular files exist

    """
    for region in ['EUR', 'JAP', 'USA']:
        batch_region(action, base_dir, region)

    return True
