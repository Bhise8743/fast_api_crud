from pydantic import BaseModel, Field,EmailStr


class UpdateContact(BaseModel):
    f_name: str = Field(pattern=r"^[A-Z]{1}\D{1,}")
    l_name: str = Field(min_length=1)
    email: EmailStr
    phone: int
    location: str = Field(default=None)

class Contact(UpdateContact):
    book: str



