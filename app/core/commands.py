import click

from app.auth.crud import create_user, get_user
from app.auth.schemas import UserCreate
from app.db.session import SessionLocal


@click.group()
def core_cli():
    pass


@core_cli.command()
def create_superuser():
    db = SessionLocal()

    user_db = get_user(db, email="root@email.com")
    if user_db is None:
        user_in = UserCreate(
            full_name="root user",
            email="root@email.com",
            password="fhw83D4hsHd0fa"
        )
        create_user(db, user_in)
    pass


@core_cli.command()
def create_default_scopes():
    pass
