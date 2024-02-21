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


@cli.command()
def create_test_db():
    """Create a test database called langchain_test used for testing purposes."""
    import psycopg2
    from psycopg2.errors import DuplicateDatabase

    # establishing the connection
    conn = psycopg2.connect(
        database="langchain",
        user="langchain",
        password="langchain",
        host="localhost",
        port="5432",
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    with conn.cursor() as cursor:
        # Preparing query to create a database
        sql = "CREATE DATABASE langchain_test;"

        # Creating a database
        try:
            cursor.execute(sql)
            print("Database created successfully.")
        except DuplicateDatabase:
            print("Database already exists")


if __name__ == "__main__":
    cli()
