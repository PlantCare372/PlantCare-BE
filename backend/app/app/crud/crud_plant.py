from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.plant import Plant
from app.schemas.plant import PlantCreate, PlantUpdate


class CRUDPlant(CRUDBase[Plant, PlantCreate, PlantUpdate]):
    def get_by_name(
        self, db: Session, *, name: str) -> Plant:
        return (
            db.query(self.model)
            .filter(Plant.name == name)
            .first()
        )

    def search(
        self, db: Session, *, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[Plant]:
        return (
            db.query(self.model)
            .filter(Plant.name.ilike(f'%{keyword}%'))
            .offset(skip)
            .limit(limit)
            .all()
        )


plant = CRUDPlant(Plant)
