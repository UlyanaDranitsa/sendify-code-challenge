from datetime import datetime
from typing import Any, List
import pydantic
from pydantic import BaseModel, Field, model_validator


class Party(pydantic.BaseModel):
    """Sender and receiver model."""
    country_code: str = Field(validation_alias="countryCode")
    country: str
    city: str
    postcode: str = Field(validation_alias="postCode")

class PackageDetails(pydantic.BaseModel):
    """Package details model."""
    pieces: int
    volume_value: float
    volume_unit: str
    weight_value: float
    weight_unit: str
    dimensions: list[Any]

    @model_validator(mode='before')
    @classmethod
    def flatten_details(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        volume = data.get("volume", {})
        weight = data.get("weight", {})

        return {
            "pieces": data.get("pieces"),
            "volume_value": volume.get("value"),
            "volume_unit": volume.get("unit"),
            "weight_value": weight.get("value"),
            "weight_unit": weight.get("unit"),
            "dimensions": data.get("dimensions", [])
        }

class Reason(pydantic.BaseModel):
    """Reason model."""
    code: str | None
    description: str | None

class Event(pydantic.BaseModel):
    """Event model."""
    code: str
    date: datetime
    location_name: str
    location_countrycode: str
    comment: str | None = None
    reasons: list[Reason]

    @model_validator(mode='before')
    @classmethod
    def flatten_event_location(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        loc = data.get("location", {})

        data["location_name"] = loc.get("name")
        data["location_countrycode"] = loc.get("countryCode")

        return data

class PackageEvent(pydantic.BaseModel):
    """Package event model."""
    code: str
    country_code: str = Field(validation_alias="countryCode")
    location: str
    date: datetime

class Package(pydantic.BaseModel):
    """Package model."""
    id: str
    events: list[PackageEvent]


class ShipmentInfo(pydantic.BaseModel):
    """Shipment info model."""
    sender: Party
    receiver: Party
    package_details: PackageDetails
    tracking_history: List[Event] = Field(default_factory=list)
    packages: List[Package] = Field(default_factory=list)

    @model_validator(mode='before')
    @classmethod
    def remap_raw_json(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        location = data.get("location", {})

        return {
            "sender": location.get("shipperPlace"),
            "receiver": location.get("consigneePlace"),
            "package_details": data.get("goods"),
            "tracking_history": data.get("events") or [],
            "packages": data.get("packages") or []
        }



