# schemas.py
from pydantic import BaseModel
from typing import List

class MovieBase(BaseModel):
    title: str
    description: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

class AttendeeBase(BaseModel):
    name: str
    email: str

class AttendeeCreate(AttendeeBase):
    pass

class Attendee(AttendeeBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str