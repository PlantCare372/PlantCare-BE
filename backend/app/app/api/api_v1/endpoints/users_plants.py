from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.UserPlant])
def read_users_plants(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users_plants.
    """

    if crud.user.is_superuser(current_user):
       users_plants = crud.user_plant.get_multi(db, skip=skip, limit=limit)
       return users_plants
 
    raise HTTPException(status_code=400, detail="Not enough permissions")




@router.get("/{id}", response_model=schemas.UserPlant)
def read_user_plant(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get user_plant by ID.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    user_plant = crud.user_plant.get(db=db, id=id)
    if not user_plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    return user_plant


