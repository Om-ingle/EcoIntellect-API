from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class TransportMode(str, Enum):
    CAR = "car"
    BIKE = "bike"
    ELECTRIC_VEHICLE = "electric_vehicle"
    MOTORCYCLE = "motorcycle"
    WALK = "walk"

class PackagingType(str, Enum):
    PLASTIC = "plastic"
    BIODEGRADABLE = "biodegradable"
    REUSABLE = "reusable"
    PAPER = "paper"

class OrderAnalysisRequest(BaseModel):
    distance_km: float = Field(..., gt=0, description="Delivery distance in kilometers")
    transport_mode: TransportMode
    packaging_type: PackagingType
    estimated_time_minutes: int = Field(..., gt=0)
    order_value: float = Field(..., gt=0)
    frequency_per_week: Optional[int] = Field(1, ge=1, le=21)

class Alternative(BaseModel):
    transport_mode: str
    packaging_type: str
    carbon_emission_grams: float
    estimated_time_minutes: int
    carbon_saved_grams: float
    time_difference_minutes: int
    eco_score: int

class YearlyProjection(BaseModel):
    total_orders_per_year: int
    total_carbon_kg: float
    trees_needed_to_offset: int
    equivalent_car_km: float
    money_spent: float
    scale_scenarios: Optional[List[dict]] = None

class OrderAnalysisResponse(BaseModel):
    carbon_emission_grams: float
    eco_score: int
    rating: str
    better_alternatives: List[Alternative]
    yearly_projection: YearlyProjection
    environmental_context: str

class CompareOptionsRequest(BaseModel):
    distance_km: float
    options: List[dict]

class UserImpactRequest(BaseModel):
    user_id: str
    time_period_days: int = 365

class UserImpactResponse(BaseModel):
    total_orders: int
    eco_score: int
    total_carbon_saved_kg: float
    rank_percentile: int
    achievements: List[str]
    yearly_projection: YearlyProjection