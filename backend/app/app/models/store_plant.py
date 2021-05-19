from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class StorePlant(Base):
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("store.id"))
    plant_id = Column(Integer, ForeignKey("plant.id"))
