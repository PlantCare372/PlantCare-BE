from typing import Any, List
from pydantic import BaseModel, EmailStr

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.config import settings
from app.utils import predict_plant_image, format_predictions

router = APIRouter()


class DetectorInput(BaseModel):
    b64image: str


@router.get("/", response_model=Any)
def get_metadata(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Metadata AI service
    """

    return {
        "host": settings.DETECTOR_HOST,
        "port": settings.DETECTOR_PORT
    }

@router.post("/", response_model=Any)
def predict(
    detector_input: DetectorInput,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Detect image.
    """

    response = predict_plant_image(detector_input.b64image)
    result = response.json()

    if "predictions" in result:
        result = format_predictions(result["predictions"])

        for i in range(0, len(result)):
            plant = crud.plant.get_by_name(db, name=result[i]["name"])
            
            if plant:    
                result[i]["id"] = plant.id
                result[i]["description"] = plant.description
                result[i]["image"] = plant.image

        return result
    else:
        raise HTTPException(status_code=500, detail="Model prediction error. Check model again")