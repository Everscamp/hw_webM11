from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field



class ContactBase(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=150)
    mobile: str = Field(max_length=50)
    email: str = Field(max_length=150)
    birthday: datetime = Field()


# class ContactUpdate(BaseModel):
#     done: bool

class ContactResponse(ContactBase):
    id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
