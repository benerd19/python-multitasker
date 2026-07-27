from pydantic import BaseModel, Field

class UserBase(BaseModel):
    pass

class UsersCreateRequest(UserBase):
    name: str
    email: str
    password: str = Field(
        min_length=8,
        max_length=16,
        pattern=r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$",
        description="Невалидный пароль"
    )
    avatar: str

class UsersCreateResponse(UserBase):
    access: str

class UsersGetInfoResponse(UserBase):
    id: int
    name: str
    email: str
    avatar: str

class UsersAuthRequest(UserBase):
    email: str
    password: str

class UsersAuthResponse(UserBase):
    access: str

class UsersPartialUpdate(UserBase):
    name: str | None = None
    password: str | None = None
    avatar: str | None = None



    



