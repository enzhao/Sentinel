from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

class CurrentUser(BaseModel):
    uid: str
    email: EmailStr
    username: str
    defaultPortfolioId: Optional[UUID] = Field(None, description="The ID of the user's default portfolio.")