import os
from typing import List

from fastapi import APIRouter, Body, Depends, File, Path, Response, UploadFile, \
    status, HTTPException

from app.common.utils.images import compress_img
from app.auth.dependencies import Auth

from app.db.dependencies import get_db
from app.universities.dependencies.buildings import get_current_building, verify_building_owner
from app.universities.dependencies.universities import get_current_university, \
    verify_university_owner
from app.universities.models import University, Building

from app.universities.crud.images import create_image, delete_image, get_image, update_image
from app.universities.schemas.buildings import BuildingCreate, \
    BuildingRetrieve
from app.universities.crud.buildings import create_building, delete_building, \
    update_building, attach_building_image, delete_building_image


router = APIRouter(prefix="/buildings")


@router.post(
    "/",
    response_model=BuildingRetrieve,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_university_owner)]
)
async def create(
    db = Depends(get_db),
    university: University = Depends(get_current_university),
    building_in: BuildingCreate = Body(...),
    auth: Auth = Depends()
):
    return create_building(db, university.id, building_in, auth.user)


@router.get("/", response_model=List[BuildingRetrieve])
async def list(university: University = Depends(get_current_university)):
    return university.buildings


@router.get("/{building_id}", response_model=BuildingRetrieve)
async def retrieve(building: Building = Depends(get_current_building)):
    return building

@router.put(
    "/{building_id}/",
    response_model=BuildingRetrieve,
    dependencies=[Depends(verify_building_owner)]
)
async def update(
    db = Depends(get_db),
    building: Building = Depends(get_current_building),
    building_in: BuildingCreate = Body(...)
):
    return update_building(db, building.id, building_in)


@router.delete(
    "/{building_id}/", dependencies=[Depends(verify_building_owner)])
async def delete(
    db = Depends(get_db),
    building: Building = Depends(get_current_building)
):
    delete_building(db, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{building_id}/images/", dependencies=[Depends(verify_building_owner)])
async def create_building_images(
    db = Depends(get_db),
    files: List[UploadFile] = File(...),
    building: Building = Depends(get_current_building)
):
    if len(building.images) + len(files) > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximun 3 images by building"
        )

    qualities = {"small": 20, "medium": 40, "original": 100}

    for file in files:
        db_image = create_image(db)
        try:
            for quality_name, quality_value in qualities.items():
                folder = f"app/static/images/buildings/{building.id}/"
                if not os.path.exists(folder):
                    os.makedirs(folder)

                _, extension = os.path.splitext(file.filename) 
                image_name = f"building_{building.id}_image_{db_image.id}_{quality_name}{extension}"
                image_path = folder + image_name

                compress_img(file.file, image_path, quality=quality_value)

                update_image(db, db_image.id, **{quality_name: "/" + image_path})

            attach_building_image(db, building.id, db_image.id) 
        except Exception as e:
            delete_image(db, db_image.id)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{building_id}/images/{image_id}/",
    dependencies=[Depends(verify_building_owner)]
)
async def remove_building_image(
    db = Depends(get_db),
    building: Building = Depends(get_current_building),
    image_id: int = Path(..., gt=0),
):
    image = get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # remove building images
    for image_path in [image.small, image.medium, image.original]:
        # remove first slash from path, it's necessary to find the file
        image_path = image_path[1:]
        if os.path.exists(image_path):
            os.remove(image_path)

    delete_building_image(db, image_id, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
