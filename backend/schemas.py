from pydantic import BaseModel, Field, field_validator
from datetime import datetime


CURRENT_YEAR = datetime.now().year


class CarInput(BaseModel):
    brand: str = Field(..., example="Toyota")
    model: str = Field(..., example="Camry")
    model_year: int = Field(..., example=2020)
    milage_ml: float = Field(..., example=30000)
    fuel_type: str = Field(..., example="Gasoline")
    accident: str = Field(..., example="None reported")
    transmission_type: str = Field(..., example="Automatic")
    HP: float = Field(..., example=203)
    Engine_L: float = Field(..., example=2.5)
    Cylinder: float = Field(..., example=4)

    @field_validator("model_year")
    @classmethod
    def validate_year(cls, v):
        if not (1990 <= v <= CURRENT_YEAR):
            raise ValueError(f"Model year must be between 1990 and {CURRENT_YEAR}")
        return v

    @field_validator("milage_ml", "HP", "Engine_L")
    @classmethod
    def validate_positive(cls, v, info):
        if v <= 0:
            raise ValueError(f"{info.field_name} must be positive")
        return v

    @field_validator("Cylinder")
    @classmethod
    def validate_cylinder(cls, v):
        if not (2 <= v <= 16):
            raise ValueError("Cylinder must be between 2 and 16")
        return v


class PredictionResponse(BaseModel):
    predicted_price: float
    currency: str = "USD"
