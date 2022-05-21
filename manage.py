import click

from app.core.commands import core_cli
from app.universities.commands import universities_cli


@click.group()
def main_cli():
    pass


main_cli.add_command(core_cli)
main_cli.add_command(universities_cli)


if __name__ == "__main__":
    main_cli()
