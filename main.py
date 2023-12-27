from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

data = []


class Contact(BaseModel):
    f_name: str
    l_name: str
    pin: int
    city: str
    state: str


@app.post('/contact', status_code=status.HTTP_201_CREATED)
def add_contact(info: Contact):
    data.append(info.model_dump())  # data go to the json file in the form of dict
    return data


@app.get('/{id}')
def get_contact(id: int):
    return data[id]


@app.put('/contact/{id}')
def update_contact(id: int, info: Contact):
    data[id] = info
    return info


@app.delete('/contact/{id}')
def del_contact(id: int):
    data.pop(id)
    return data
