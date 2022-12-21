import click

from .insert_initial_data import insert_initial_data
from .upload_unicor_imgs import upload_unicor_imgs


@click.group()
def cli():
    pass


cli.add_command(insert_initial_data)
cli.add_command(upload_unicor_imgs)
