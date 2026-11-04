from sqlmodel import SQLModel, Field
from typing import Optional

# jinja  2-------------------------------

class CreateUser(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    email: str 
    phone: str


# ---------------------------------
# class User(SQLModel,table=True):
#     id: Optional[int] = Field(default=None,primary_key=True)
#     name: str
#     email: str = Field(unique=True, index=True)
#     hashed_password: str