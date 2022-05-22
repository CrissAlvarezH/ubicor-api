import click

from .insert_initial_data import insert_initial_data


@click.group()
def cli():
    pass


cli.add_command(insert_initial_data)
