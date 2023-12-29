import json
from typing import Union

from fastapi import FastAPI, status, Depends
from fastapi.responses import Response

from sqlalchemy.orm import Session
from model import get_db, Book, Contact
from schema import UpdateContact, Contact as ContactSchema

app = FastAPI()


@app.get('/get', status_code=status.HTTP_200_OK)
def retrieve_contact(response: Response, db: Session = Depends(get_db), book: Union[int, None] = None):
    try:
        contacts = db.query(Contact).filter_by(book_id=book).all() if book else db.query(Contact).all()
        return {'message': "Data retrieved ", 'status': 200, 'data': contacts}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


@app.post('/post', status_code=status.HTTP_201_CREATED)
def add_contact(body: ContactSchema, response: Response,
                db: Session = Depends(get_db)):  # db session dependency on get_db
    try:
        body = body.model_dump()  # transform the schema into dict
        b_name = body.pop('book')  # it takes the book dict
        book = db.query(Book).filter_by(b_name=b_name).one_or_none()
        if not book:
            book = Book(b_name=b_name)
            db.add(book)
            db.commit()  # if you are not committed then this book will be rollback
        body.update(book_id=book.id)
        contact = Contact(**body)  # kwargs
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return {'message': 'Contact Added ', 'status': 201, 'data': contact}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


# @app.put('/put', status_code=status.HTTP_200_OK)
# def update_contact(body: UpdateContact, response: Response, db: Session = Depends(get_db)):
#     try:
#         contact = db.query(Contact).filter_by(f_name=body.f_name).one()
#         if contact:
#             list(map(lambda item: setattr(contact, item[0], item[1]), body.model_dump().items()))         # setattr(object, field, value)
#         db.commit()
#         db.refresh(contact)
#         return {'message': 'Contact Updated ', 'status': 200, 'data': contact}
#     except Exception as ex:
#         response.status_code = 400
#         return {'message': str(ex), 'status': 400}


@app.put('/put/{contact_id}',status_code=status.HTTP_200_OK)
def update_contact(contact_id:int,updated_cont:UpdateContact,response:Response,db:Session = Depends(get_db)):
    try:
        ex_contact = db.query(Contact).filter_by(id=contact_id).first()
        if not ex_contact:
            raise Exception('Contact not found ')
        for field,value in updated_cont.model_dump(exclude_unset=True).items():
            setattr(ex_contact,field,value)
        db.commit()
        db.refresh(ex_contact)
        return {'message':"Contact Updated ",'status':200,'data':ex_contact}
    except Exception as ex:
        response.status_code = 400
        return {'message':str(ex),'status':400}


@app.delete('/del/{contact_id}',status_code=status.HTTP_200_OK)
def delete_contact(contact_id:int,response:Response,db: Session = Depends((get_db))):
    try:
        contact = db.query(Contact).filter_by(id=contact_id).first()
        if not contact:
            raise Exception("Contact not found")
        db.delete(contact)
        db.commit()
        return {'message':'Contact deleted ','status':200}

    except Exception as ex:
        response.status_code=400
        return {'message':str(ex),'status':400}

































"""
@app.get('/get', status_code=status.HTTP_200_OK)
def retrieve_all_contacts(response: Response):
    try:
        with open('addressbook.json') as file:
            data = json.load(file)
        return {'message': 'Data Retrieved ', 'status': 200, 'data': data}
    except FileNotFoundError:
        response.status_code = 400
        return {'message': 'File Not Found', 'status': 400}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}

@app.get('/get/book',status_code=status.HTTP_200_OK)
def retrieve_all_contacts_in_a_book(con:Contact,response:Response):
    try:
        with open('addressbook.json') as file:
            data = json.load(file)
            if con.book in data:
                book = data.get(con.book)
                return {'message':"Book Retrieved ",'status':200,'data':book}
            else:
                raise Exception("This Book is not present ")
    except FileNotFoundError:
        response.status_code = 400
        return {'message': 'File Not Found', 'status': 400}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}


@app.put('/put',status_code=status.HTTP_200_OK)
def update_a_contact(con: Contact,response:Response):
    try:
        with open('addressbook.json') as file:
            db_contacts = json.load(file)
        if con.book in db_contacts:
            book = db_contacts.get(con.book)
            if book.get(con.f_name):
                book.update({con.f_name:con.model_dump()})
            else:
                raise Exception("Contact Not Present ")
        else:
            raise Exception("This Book is not present ")
        with open("addressbook.json",'w') as file:
            json.dump(db_contacts,file,indent=4)
            return {'message':'Contact update successfully...','status':201,'data':con.model_dump()}
    except FileNotFoundError:
        response.status_code = 500
        return {'message':'File Not found ','status':500}
    except Exception as ex:
        response.status_code = 400
        return {'message':str(ex),'status':400}


        
@app.delete('/del/{book}/{name}',status_code=status.HTTP_200_OK)
def del_contact_in_a_book(book:str,name:str,response:Response):
    try:
        with open('addressbook.json') as file:
            data = json.load(file)
        if book in data:
            book_obj = data.get(book)
            if name in book_obj:
                book_obj.pop(name)
                data.update({book:book_obj})
            else:
                raise Exception("Contact not found")
        else:
            raise Exception("Book not found")
        with open('addressbook.json','w') as file:
            json.dump(data,file,indent=4)
            return {'message':"Contact deleted successfully ",'status':200}
    except FileNotFoundError:
        response.status_code = 400
        return {'message': 'File Not Found', 'status': 400}
    except Exception as ex:
        response.status_code = 400
        return {'message': str(ex), 'status': 400}

"""

"""
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
"""
