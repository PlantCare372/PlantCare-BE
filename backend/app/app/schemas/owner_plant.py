from typing import Optional

from pydantic import BaseModel


# Shared properties
class OwnerPlantBase(BaseModel):
    user_id: int
    plant_id: int


# Properties to receive on user_plant creation
class OwnerPlantCreate(OwnerPlantBase):
    pass

# Properties to receive on user_plant update
class OwnerPlantUpdate(OwnerPlantBase):
    pass


# Properties shared by models stored in DB
class OwnerPlantInDBBase(OwnerPlantBase):
    id: int
    user_id: int
    plant_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class OwnerPlant(OwnerPlantInDBBase):
    pass


# Properties properties stored in DB
class OwnerPlantInDB(OwnerPlantInDBBase):
    pass
