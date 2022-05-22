import click

from app.auth.crud import create_user, get_user
from app.auth.schemas import UserCreate
from app.db.session import SessionLocal


@click.group()
def cli():
    pass


@cli.command()
def create_superuser():
    click.echo("\nINIT create superuser")
    db = SessionLocal()

    user_db = get_user(db, email="root@email.com")
    if user_db is not None:
        click.echo("superuser already exist")
    else:
        user_in = UserCreate(
            full_name="root user",
            email="root@email.com",
            password="fhw83D4hsHd0fa"
        )
        create_user(db, user_in)

    db.close()
    click.echo("FINISH create superuser")


@cli.command()
def create_default_scopes():
    pass
