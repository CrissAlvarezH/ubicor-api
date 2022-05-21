import click

from .insert_initial_data import insert_initial_data


@click.group()
def universities_cli():
    pass


universities_cli.add_command(insert_initial_data)
