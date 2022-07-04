import click

from app.auth.crud import create_user, get_user
from app.auth.schemas import UserCreate
from app.db.session import SessionLocal

from .config import settings

@click.group()
def cli():
    pass


@cli.command()
def create_superuser():
    click.echo("\nINIT create superuser")
    db = SessionLocal()

    user_db = get_user(db, email=settings.SUPER_USER_EMAIL)
    if user_db is not None:
        click.echo("superuser already exist")
    else:
        user_in = UserCreate(
            full_name="root user",
            email=settings.SUPER_USER_EMAIL,
            password=settings.SUPER_USER_PASSWORD
        )
        create_user(db, user_in)

    db.close()
    click.echo("FINISH create superuser")


@cli.command()
def create_default_scopes():
    pass
