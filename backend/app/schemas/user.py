from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=255,
    )

    password: str = Field(
        min_length=12,
        max_length=128,
    )


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool

    model_config = {
        "from_attributes": True
    }