from typing import Optional

from pydantic import BaseModel


# Shared properties
class UserPlantBase(BaseModel):
    user_id: int
    plant_id: int


# Properties to receive on user_plant creation
class UserPlantCreate(UserPlantBase):
    pass

# Properties to receive on user_plant update
class UserPlantUpdate(UserPlantBase):
    pass


# Properties shared by models stored in DB
class UserPlantInDBBase(UserPlantBase):
    id: int
    user_id: int
    plant_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class UserPlant(UserPlantInDBBase):
    pass


# Properties properties stored in DB
class UserPlantInDB(UserPlantInDBBase):
    pass
