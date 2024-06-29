from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description="User login", alias='login')
    reset_token: str = Field(None, description="Password reset token", alias='token')
    password: str = Field(..., description="Current password", alias='oldPassword')
    new_password: str = Field(..., description="New password", alias='newPassword')
