import click

from app.auth.crud import add_scope_to_user, create_user, get_user, create_scope, \
    get_scope, list_scopes
from app.auth.schemas import UserCreate
from app.auth.scopes import CREATE_BUILDINGS, CREATE_UNIVERSITIES, EDIT_BUILDINGS, \
    EDIT_UNIVERSITIES, EDIT_USERS, LIST_USERS
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
        user = create_user(db, user_in)

        # add scopes
        scopes = list_scopes(db)
        for scope in scopes:
            add_scope_to_user(db, user.id, scope.name)

    db.close()
    click.echo("FINISH create superuser")


@cli.command()
def create_default_scopes():
    db = SessionLocal()

    default_scopes = [
        LIST_USERS, EDIT_USERS,
        CREATE_UNIVERSITIES, EDIT_UNIVERSITIES,
        CREATE_BUILDINGS, EDIT_BUILDINGS
    ]

    for scope in default_scopes:
        if not get_scope(db, scope):
            create_scope(db, scope)

    db.close()
