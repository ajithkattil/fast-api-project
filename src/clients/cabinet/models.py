from pydantic import BaseModel, Field


class CabinetDataAttributes(BaseModel):
    activates_at: str = Field(..., alias="activates-at")
    deactivated_at: str | None = Field(None, alias="deactivates-at")
    plan_description: str = Field(..., alias="plan-description")
    plan_id: int = Field(..., alias="plan-id")
    short_code: str = Field(..., alias="short-code")


class CabinetDataItem(BaseModel):
    type: str
    id: str
    attributes: CabinetDataAttributes


class CabinetResponse(BaseModel):
    data: list[CabinetDataItem]


class CabinetCycleAttributes(BaseModel):
    date: str
    is_active: bool = Field(alias="is-active")


class CabinetCycleItem(BaseModel):
    id: str
    attributes: CabinetCycleAttributes


class CabinetCycleResponse(BaseModel):
    data: list[CabinetCycleItem]
