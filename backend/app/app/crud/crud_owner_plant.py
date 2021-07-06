from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.owner_plant import OwnerPlant
from app.models.plant import Plant
from app.schemas.owner_plant import OwnerPlantCreate, OwnerPlantUpdate


class CRUDOwnerPlant(CRUDBase[OwnerPlant, OwnerPlantCreate, OwnerPlantUpdate]):
    def get_multi_by_user_id(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Plant]:
        return (
            db.query(Plant)
            .join(OwnerPlant)
            .filter(OwnerPlant.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


owner_plant = CRUDOwnerPlant(OwnerPlant)
