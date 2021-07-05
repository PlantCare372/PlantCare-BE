from typing import Optional

from pydantic import BaseModel

import datetime

# Shared properties
class UserReminderBase(BaseModel):
    user_id: int
    plant_id: int


# Properties to receive on user_plant creation
class UserReminderCreate(UserReminderBase):
    user_id: int
    plant_id: int
    detail_reminder_time: datetime.datetime
    pass

# Properties to receive on user_plant update
class UserReminderUpdate(UserReminderBase):
    pass


# Properties shared by models stored in DB
class UserReminderInDBBase(UserReminderBase):
    id: int
    user_id: int
    plant_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class UserReminder(UserReminderInDBBase):
    pass


# Properties properties stored in DB
class UserReminderInDB(UserReminderInDBBase):
    pass
