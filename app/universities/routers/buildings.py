import logging
from typing import List

from fastapi import APIRouter, Body, Depends, File, Path, Response, UploadFile, \
    status, HTTPException

from app.auth.dependencies import Auth

from app.db.dependencies import get_db
from app.universities.dependencies.buildings import get_current_building, verify_building_owner
from app.universities.dependencies.universities import get_current_university, \
    verify_university_owner
from app.universities.models import University, Building

from app.universities.crud.images import create_image, delete_image, get_image, update_image
from app.universities.schemas.buildings import BuildingCreate, BuildingImageRetrieve, \
    BuildingList, BuildingRetrieve, ImageRetrieve
from app.universities.crud.buildings import create_building, delete_building, \
    update_building, attach_building_image, delete_building_image
from app.universities.utils.images import delete_building_image_file, \
    is_valid_image, save_building_image_file


LOG = logging.getLogger("universities.routers")


router = APIRouter(prefix="/buildings")


@router.post(
    "/",
    response_model=BuildingList,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_university_owner)]
)
async def create(
    db=Depends(get_db),
    university: University = Depends(get_current_university),
    building_in: BuildingCreate = Body(),
    auth: Auth = Depends()
):
    return create_building(db, university.id, building_in, auth.user)


@router.get("/", response_model=List[BuildingList])
async def list(university: University = Depends(get_current_university)):
    return [b for b in university.buildings if b.is_active]


@router.get("/{building_id}", response_model=BuildingRetrieve)
async def retrieve(building: Building = Depends(get_current_building)):
    return building


@router.put(
    "/{building_id}/",
    response_model=BuildingList,
    dependencies=[Depends(verify_building_owner)]
)
async def update(
    db=Depends(get_db),
    building: Building = Depends(get_current_building),
    building_in: BuildingCreate = Body()
):
    return update_building(db, building.id, building_in)


@router.delete(
    "/{building_id}/", dependencies=[Depends(verify_building_owner)])
async def delete(
    db=Depends(get_db),
    building: Building = Depends(get_current_building)
):
    delete_building(db, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{building_id}/images/",
    response_model=List[BuildingImageRetrieve],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_building_owner)]
)
async def create_building_images(
    db=Depends(get_db),
    files: List[UploadFile] = File(),
    building: Building = Depends(get_current_building)
):
    if len(building.building_images) + len(files) > 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximun 3 images by building"
        )

    for file in files:
        is_valid, error = is_valid_image(file)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error)

        db_image = create_image(db)
        try:
            image_paths = save_building_image_file(file, building.id, db_image.id) 

            update_image(db, db_image.id, **image_paths)
            attach_building_image(db, building.id, db_image.id)
        except Exception as e:
            LOG.error(f"Error on create bulding image: {str(e)}")
            LOG.exception(e)
            delete_image(db, db_image.id)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return building.building_images


@router.put(
    "/{building_id}/images/{image_id}/",
    response_model=ImageRetrieve,
    dependencies=[Depends(verify_building_owner)]
)
async def update_building_image(
    db=Depends(get_db),
    file: UploadFile = File(),
    building: Building = Depends(get_current_building),
    image_id: int = Path(gt=0)
):
    is_valid, error = is_valid_image(file)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    image = get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        save_building_image_file(file, building.id, image.id)
    except Exception as e:
        LOG.error(f"Error on update bulding image: {str(e)}")
        LOG.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return image


@router.delete(
    "/{building_id}/images/all/",
    dependencies=[Depends(verify_building_owner)]
)
async def remove_all_building_images(
    db=Depends(get_db),
    building: Building = Depends(get_current_building),
):
    for building_image in building.building_images:
        delete_building_image_file(building_image.image)
        delete_building_image(
            db, building_image.image.id, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{building_id}/images/{image_id}/",
    dependencies=[Depends(verify_building_owner)]
)
async def remove_building_image(
    db=Depends(get_db),
    building: Building = Depends(get_current_building),
    image_id: int = Path(gt=0),
):
    image = get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    delete_building_image_file(image)
    delete_building_image(db, image_id, building.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
