from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, defer

from app.crud.base import CRUDBase

from app.models.user_reminder import UserReminder
from app.models.plant import Plant
from app.schemas.user_reminder import UserReminderCreate, UserReminderUpdate

import datetime

class CRUDUserReminder(CRUDBase[UserReminder, UserReminderCreate, UserReminderUpdate]):
    def get_multi_by_user_id(self, db: Session, *, user_id: int, plant_id: int = None):
        query = (
            db.query(UserReminder)
            .options(defer('user_id'),defer('status'))
            .filter(UserReminder.user_id == user_id)
            .order_by(UserReminder.detail_reminder_time.asc())
        )

        if plant_id:
            query = query.filter(UserReminder.plant_id == plant_id)

        results = query.all()

        final_result = []

        for result in results:
            if result.detail_reminder_time > datetime.datetime.now():
                final_result.append(result)
        
        return final_result



user_reminder = CRUDUserReminder(UserReminder)
