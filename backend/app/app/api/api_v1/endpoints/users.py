from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

from datetime import datetime
import stripe


router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """

    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/payment/buy")
def buy_plant(
    payment: schemas.UserPayment,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user.
    """

    stripe.api_key = 'sk_test_51JA8KZE7avB6EvajjeSP7jogYeO6sX2dTM6ryhg5wdS1D6aX0RNLDF2Lq8KDOFdP944aAnWvoCVDFjYfVR7qzBZz00jdIkltxr' #Your test/live secret key

    payment_intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        payment_method = payment.payment_method_id,
        amount=payment.price,
        application_fee_amount=140,
        currency='usd',
        stripe_account='acct_1JA8TU2QNSk8WjAB',#connected account ID
        receipt_email=payment.email,
        confirm=True
    )

    return {
        "client_secret": payment_intent.client_secret
    }


@router.get("/add-reminder/{plant_id}")
def add_to_favorites(
    plant_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Add reminder to user
    """

    plant = crud.plant.get(db, id=plant_id)

    if not plant:
        raise HTTPException(
            status_code=401,
            detail="Plant not exist",
        )

    if not plant.reminder_time:
        raise HTTPException(
            status_code=401,
            detail="Plant don't have schedule time",
        )

    reminder = crud.user_reminder.get_multi_by_user_id(db, user_id=current_user.id, plant_id=plant_id)

    if len(reminder) > 0:
        raise HTTPException(
            status_code=401,
            detail="Reminder added for two week",
        )

    [hour, minute] = plant.reminder_time.split(":")

    now = datetime.now()


    for i in range(1, 15):
        planned_time = now.replace(day=now.day + i, hour=int(hour), minute=int(minute))
        crud.user_reminder.create(db, obj_in=schemas.UserReminderCreate(user_id=current_user.id, plant_id=plant_id, detail_reminder_time=planned_time))

    return {"message": "Add reminder successfully"}


@router.get("/reminder")
def add_to_favorites(
    plant_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Add reminder to user
    """

    return crud.user_reminder.get_multi_by_user_id(db, user_id=current_user.id, plant_id=plant_id)



@router.get("/add-to-favorites/{plant_id}", response_model=schemas.Plant)
def add_to_favorites(
    plant_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Add plant to user
    """
    if not crud.user_plant.is_favourited_plant(db, user_id=current_user.id, plant_id=plant_id):
        plant = crud.plant.get(db, plant_id)

        if plant:
            user_plant_in = schemas.UserPlantCreate(user_id=current_user.id, plant_id=plant_id)
            user_plant = crud.user_plant.create(db, obj_in=user_plant_in)

            return plant
        else:
            raise HTTPException(status_code=401, detail="Plant is not exist in database")
    
    raise HTTPException(status_code=200, detail="Plant is also exist in your favourite list")

@router.get("/get-favorited-plants", response_model=List[schemas.Plant])
def get_favorited_plants(
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get favourited plants
    """

    plants = crud.user_plant.get_multi_by_user_id(db, user_id=current_user.id, skip=skip, limit=limit)
    
    return plants

@router.get("/remove-from-favorites/{plant_id}", response_model=Any)
def remove_from_favorites(
    plant_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Remove plants from favorites
    """

    plant = crud.plant.get(db, plant_id)
    if not plant:
        raise HTTPException(status_code=401, detail="Plant is not exist in database")

    user_plant = crud.user_plant.is_favourited_plant(db, user_id=current_user.id, plant_id=plant_id)
    if not user_plant:
        raise HTTPException(status_code=200, detail="Plant is not exist in your favorites")
 
    user_plant = crud.user_plant.remove(db, id=user_plant.id)

    return {
        "message": "Delete successfully"
    }
    

@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


