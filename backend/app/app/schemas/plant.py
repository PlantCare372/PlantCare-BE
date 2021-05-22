from typing import Optional

from pydantic import BaseModel


# Shared properties
class PlantBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    temperature: Optional[str] = None
    light: Optional[str] = None
    humidity: Optional[str] = None
    wind: Optional[str] = None


# Properties to receive on plant creation
class PlantCreate(PlantBase):
    name: str


# Properties to receive on plant update
class PlantUpdate(PlantBase):
    pass


# Properties shared by models stored in DB
class PlantInDBBase(PlantBase):
    id: int
    name: str
    description: str
    temperature: Optional[str] = None
    light:  Optional[str] = None
    humidity:  Optional[str] = None
    wind:  Optional[str] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Plant(PlantInDBBase):
    pass


# Properties properties stored in DB
class PlantInDB(PlantInDBBase):
    pass
