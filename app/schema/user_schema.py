from pydantic import BaseModel, Field, EmailStr, model_validator


class UserBase(BaseModel):
    email: EmailStr = Field(default=None)


class UserCreate(UserBase):
    name: str = Field(default=None)
    password: str = Field(default=None)
    password_confirm: str = Field(default=None)

    @model_validator(mode="after")
    def do_passwords_match(self) -> "UserCreate":
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Passwords do not match.")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "name": "admin",
                "email": "admin@example.com",
                "password": "123newnew",
                "password_confirm": "123newnew"
            }
        }


class UserLogin(UserBase):
    password: str = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "123newnew",
            }
        }


class UserResponse(UserBase):
    id: int
    name: str

    class Config:
        from_attributes = True
