from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="NGN", min_length=3, max_length=3)
    beneficiary: str = Field(min_length=1, max_length=255)

    model_config = ConfigDict(extra="forbid")


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    currency: str
    beneficiary: str
    status: str

    model_config = ConfigDict(from_attributes=True)
