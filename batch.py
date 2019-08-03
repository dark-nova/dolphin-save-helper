from pathlib import Path


def batch_region(action, base_dir: str, region: str, card_slot: str):
    """Performs an `action` repeatedly across a given `region` and
    `card_slot`.

    Before using this function, ensure all parameters are valid.

    Args:
        action (function): the function to run in batch
        base_dir (str): the base dir created and used by Dolphin Emulator
        region (str): 'EUR', 'JAP', 'USA'
        card_slot (str): either 'Card A' or 'Card B'

    Returns:
        bool: True

    Raises:
        Exception: if `action` fails at any given time, or
        regular files exist

    """
    card_dir = Path(base_dir) / 'GC' / region / card_slot
    failure = []
    for file in card_dir.glob('*.gci'):
        if file.is_symlink():
            action(base_dir, region, card_slot)
        else:
            failure.append(file.name)

    if failure:
        raise Exception(
            f"""You have regular files to manually delete or move:
            {' '.join(failure)}"""
            )
    else:
        return True


def batch_region_all(action, base_dir: str, region: str):
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
        batch_region(action, base_dir, region, f'Card {slot}')

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
        batch_region_all(action, base_dir, region)

    return True
