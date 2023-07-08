"""Glacier management utilities."""
from pathlib import Path
from typing import Any

import boto3
from tqdm import tqdm

LAST_DELETED_TEMPLATE = "last-deleted-{vault}"


def delete_archives(vault: str, inventory: dict[str, Any]) -> None:
    """Delete all the archives from a glacier vault.

    Params
    ------
    vault: The name of the vault to clear from archives.
    inventory: The parsed JSON output of the inventory retrieval job.
    """
    cache_file = Path(f"./{LAST_DELETED_TEMPLATE}".format(vault=vault))
    if cache_file.exists():
        seen_last = False
        last_deleted = cache_file.read_text().strip()
    else:
        seen_last = True
        last_deleted = None

    glacier = boto3.client("glacier")

    for archive in tqdm(inventory["ArchiveList"]):
        if not seen_last:
            if archive["ArchiveId"] == last_deleted:
                seen_last = True
            continue

        glacier.delete_archive(vaultName=vault, archiveId=archive["ArchiveId"])
        cache_file.write_text(archive["ArchiveId"])

    cache_file.unlink()
