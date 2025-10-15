from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


@dataclass
class Order:
    id: str
    arrival_date: datetime
    fulfillable: bool
    shipping_address: ShippingAddress
    recipes: list[OrderRecipe]
    brand: str | None = None
    fulfillment_options: FulfillmentOptions | None = None
    sales_channel_id: str | None = None


@dataclass
class FulfillmentOptions:
    delivery_option_token: str | None = None
    special_handlings: list[SpecialHandlings] | None = None


class SpecialHandlings(StrEnum):
    WHITE_GLOVE_BOX = "WHITE_GLOVE_BOX"
    GUARANTEED_DELIVERY = "GUARANTEED_DELIVERY"


class LocationType(StrEnum):
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"


@dataclass
class PostalAddress:
    postal_code: str
    administrative_area: str
    locality: str
    address_lines: list[str]
    recipients: list[str]


@dataclass
class ContactNumber:
    phone_number: str


@dataclass
class ShippingAddress:
    postal_address: PostalAddress
    contact_number: ContactNumber
    location_type: LocationType
    delivery_instructions: str | None = None


@dataclass
class OrderRecipe:
    quantity: int
    recipe_sku: str
