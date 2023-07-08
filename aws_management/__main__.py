"""Management script."""
import json
from typing import TextIO

import click

import aws_management.glacier


@click.group()
def cli() -> None:
    ...


@cli.group()
def glacier() -> None:
    ...


@glacier.command()
@click.argument("vault")
@click.argument("inventory", type=click.File("r"))
def delete_archives(vault: str, inventory: TextIO) -> None:
    """Delete archives from a vault.

    Params
    ------
    vault: The name of the vault.
    inventory: An open file-like object containing the inventory data.
    """
    inventory_data = json.load(inventory)
    aws_management.glacier.delete_archives(vault, inventory_data)


if __name__ == "__main__":
    cli()
