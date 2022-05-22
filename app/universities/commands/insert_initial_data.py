import json
import os
from typing import List

import click

from app.db.session import SessionLocal
from app.universities.crud.university import create_university, get_university_by_slug
from app.universities.crud.buildings import create_building, create_building_zone, \
    get_building_zone
from app.universities.crud.rooms import create_room
from app.universities.schemas.buildings import BuildingCreate
from app.universities.schemas.rooms import RoomCreate
from app.universities.schemas.universities import UniversityCreate
from app.auth.crud import get_user


@click.command()
def insert_initial_data():
    click.echo("\nINIT insert initial data")
    dirname = os.path.dirname(__file__)
    data_path = os.path.join(dirname, "initial_data.json")
    with open(data_path, "r") as f:
        data = json.loads(f.read())

    class BuildingData(BuildingCreate):
        rooms: List[RoomCreate]

    class UniversityData(UniversityCreate):
        buildings: List[BuildingData]

    data = [UniversityData(**u) for u in data]

    db = SessionLocal()
    user = get_user(db, email="root@email.com")

    for university_data in data:
        university = get_university_by_slug(db, university_data.slug)
        if university is not None:
            click.echo(f"University with slug '{university.slug}' already exists")
            continue

        university = create_university(
            db,
            university_in=UniversityCreate(**university_data.dict()),
            creator=user
        )

        for building_data in university_data.buildings:
            zone = get_building_zone(db, building_data.zone)
            if zone is None:
                create_building_zone(db, building_data.zone)

            building = create_building(
                db,
                university_id=university.id,
                building_in=BuildingCreate(**building_data.dict()),
                creator=user
            )

            for room_data in building_data.rooms:
                create_room(
                    db,
                    building_id=building.id,
                    room_in=room_data,
                    creator_id=user.id
                )
    db.close()

    click.echo("FINISH insert initial data")