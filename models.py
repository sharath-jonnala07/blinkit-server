from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class HouseholdProfile(BaseModel):
    user_id: Optional[str] = "user_default"
    people: List[str] = Field(default_factory=list)          # ["Family", "Guests", "Pets"]
    rooms: List[str] = Field(default_factory=list)           # ["Kitchen", "Living Area", "Bedrooms", "Restroom", "Gym", ...]
    home_descriptors: List[str] = Field(default_factory=list) # ["Fitness-focused", "Busy professionals", ...]
    monthly_goals: List[str] = Field(default_factory=list)    # ["Eat healthier", "Save time", "Stay fit", ...]
    routines: List[str] = Field(default_factory=list)         # ["Breakfast", "Laundry", "Fitness", "Snacks", "Wind-down"]
    events: List[str] = Field(default_factory=list)           # ["Festivals", "Birthdays", "Celebrations", "Weekend Brunch"]
    specific_help: Optional[str] = ""

class Product(BaseModel):
    id: str
    brand: str
    name: str
    meta: str
    price: float
    strike: Optional[float] = None
    rating: float
    tags: List[str]
    description: Optional[str] = ""

class HouseholdMission(BaseModel):
    id: str
    title: str
    subtitle: str
    eyebrow: str
    target_room: str
    target_routine: str
    match_score: float = 0.0
    recommended_product_ids: List[str]
    cta: str

class RecommendationResponse(BaseModel):
    profile: HouseholdProfile
    top_mission_slugs: List[str]
    missions: List[HouseholdMission]
    priority_products: List[Product]
    persona_tag: str
    recommendation_rationale: str
