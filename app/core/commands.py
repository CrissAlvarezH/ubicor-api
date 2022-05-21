import click


@click.group()
def core_cli():
    pass


@core_cli.command()
def create_superuser():
    pass


@core_cli.command()
def create_default_scopes():
    pass
