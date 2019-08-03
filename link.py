from pathlib import Path


def link_files(sub_dir: str, base_dir: str, card_slot: str, region: str):
    """Link files from `sub_dir` into `base_dir` / `card_slot`.
    If `card_slot` doesn't exist, create it.

    Due to requiring `sub_dir` and `base_dir` for processing,
    `link_files` cannot be used in batch.

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
        print(f'{card_dir.name} doesn\'t exist! Creating...')
        card_dir.mkdir(parents=True)

    for file in sub_dir.glob(GCI_GLOB):
        current = card_dir / file.name
        current.symlink_to(file)
        print(f'Linked {file.name}!')

    return True
