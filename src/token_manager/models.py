from pydantic import BaseModel, ConfigDict, Field


class Param(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str = Field(alias="Name")
    value: str = Field(alias="Value")


class ParamResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parameters: list[Param] = Field(alias="Parameters")
    invalid_parameters: list[str] | None = Field(default=None, alias="InvalidParameters")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    created_at: int
    id_token: str
