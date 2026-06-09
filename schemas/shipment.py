from pydantic import BaseModel, Field
from typing import Optional, List

class ShipmentRequest(BaseModel):
    """Structured output schema - This is your GOLD layer"""
    shipment_id: Optional[str] = Field(None, description="Shipment or load number")
    origin: str = Field(..., description="Pickup city/state or address")
    destination: str = Field(..., description="Delivery city/state or address")
    carrier: Optional[str] = Field(None, description="Carrier name")
    load_type: Optional[str] = Field(None, description="Dry Van, Reefer, Flatbed, etc.")
    weight: Optional[float] = Field(None, description="Weight in lbs")
    pickup_date: Optional[str] = Field(None, description="Pickup date (YYYY-MM-DD)")
    delivery_date: Optional[str] = Field(None, description="Delivery date (YYYY-MM-DD)")
    status: Optional[str] = Field(None, description="Current status")
    exceptions: List[str] = Field(default_factory=list, description="Any issues or special notes")
    confidence: float = Field(..., description="Model's confidence score 0.0 to 1.0")