"""Tests for aws_management.glacier."""
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

import aws_management.glacier


@pytest.fixture(autouse=True)
def client() -> Iterator[MagicMock]:
    mock_obj = MagicMock()
    with patch.object(aws_management.glacier.boto3, "client", return_value=mock_obj):
        yield mock_obj


@pytest.fixture
def inventory() -> dict[str, Any]:
    return {"ArchiveList": [{"ArchiveId": str(i)} for i in range(100)]}


def test_delete_archives(client: MagicMock, inventory: dict[str, Any]) -> None:
    """Test delete_archives"""
    aws_management.glacier.delete_archives("vault", inventory)

    assert len(client.mock_calls) == len(inventory["ArchiveList"])
    assert not Path("./last-deleted-vault").exists()

def test_delete_archives_halfway(client: MagicMock, inventory: dict[str, Any]) -> None:
    """Test delete_archives with an in-progress last-deleted file"""
    with open("./last-deleted-vault", "w") as fp:
        print(49, file=fp)

    aws_management.glacier.delete_archives("vault", inventory)

    assert len(client.mock_calls) == len(inventory["ArchiveList"]) - 50
    assert not Path("./last-deleted-vault").exists()
