"""Command-line interface."""
import click

from gmn_data_store.setup_database import setup_database as _setup_database


@click.group()
@click.version_option()
def main() -> None:
    """GMN Data Store."""


@main.command()
def setup_database() -> None:
    """Setup database."""
    _setup_database()  # pragma: no cover


if __name__ == "__main__":
    main()  # pragma: no cover
