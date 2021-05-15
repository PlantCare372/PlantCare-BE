from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Plant])
def read_plants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve plants.
    """
    # if crud.user.is_superuser(current_user):
    plants = crud.plant.get_multi(db, skip=skip, limit=limit)
    # else:
    #     plants = crud.plant.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    return plants


@router.get("/search", response_model=List[schemas.Plant])
def read_plant(
    *,
    q: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search plant by name.
    """

    plants = crud.plant.search(db, keyword=q, skip=skip, limit=limit)

    return plants

@router.get("/{id}", response_model=schemas.Plant)
def read_plant(
    *,
    id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get plant by ID.
    """
    plant = crud.plant.get(db=db, id=id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    # if not crud.user.is_superuser(current_user) and (plant.owner_id != current_user.id):
        # raise HTTPException(status_code=400, detail="Not enough permissions")
    return plant


