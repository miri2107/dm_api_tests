from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class Registration(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description="User login", alias='login')
    password: str = Field(..., description="User password")
    email: str = Field(..., description="User email")
