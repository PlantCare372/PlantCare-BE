from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.user_plant import UserPlant
from app.models.plant import Plant
from app.schemas.user_plant import UserPlantCreate, UserPlantUpdate


class CRUDUserPlant(CRUDBase[UserPlant, UserPlantCreate, UserPlantUpdate]):
    def get_multi_by_user_id(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Plant]:
        return (
            db.query(Plant)
            .join(UserPlant)
            .filter(UserPlant.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def is_favourited_plant(self, db: Session, *, user_id: int, plant_id: int) -> UserPlant:
        return db.query(self.model).filter(UserPlant.user_id == user_id).filter(UserPlant.plant_id == plant_id).first()
        


user_plant = CRUDUserPlant(UserPlant)
