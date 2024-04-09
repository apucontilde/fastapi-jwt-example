from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserSession(BaseModel):
    user_id: int
    access_token: str


class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserSchema(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
