from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Plant(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=False)
    image = Column(String, index=False)
    temperature = Column(String, index=False)
    light = Column(String, index=False)
    humidity = Column(String, index=False)
    wind = Column(String, index=False)

    

