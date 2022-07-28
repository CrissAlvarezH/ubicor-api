""" Generate global cli automatically """
from importlib import import_module

import click

from app.core.config import COMMAND_LOCATIONS


def manage_commands():
    @click.group()
    def main_cli():
        pass

    for location in COMMAND_LOCATIONS:
        commands = import_module(f"app.{location}.commands")
        module_cli = getattr(commands, "cli")
        main_cli.add_command(module_cli, location)

    return main_cli


if __name__ == "__main__":
    main_cli = manage_commands()
    main_cli()
