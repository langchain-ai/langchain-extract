#!/usr/bin/env python
"""Run migrations."""
import click

from db.models import ENGINE, Base


@click.group()
def cli():
    """Database migration commands."""
    pass


@cli.command()
def create():
    """Create all tables."""
    Base.metadata.create_all(ENGINE)
    click.echo("All tables created successfully.")


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to drop all tables?")
def drop():
    """Drop all tables."""
    Base.metadata.drop_all(ENGINE)
    click.echo("All tables dropped successfully.")


if __name__ == "__main__":
    cli()
