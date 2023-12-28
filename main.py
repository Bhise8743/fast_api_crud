import json
from fastapi import FastAPI, status
from fastapi.responses import Response
from schema import Contact

app = FastAPI()


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


@app.post('/post', status_code=status.HTTP_201_CREATED)
def add_contact(con: Contact, response: Response):
    try:
        with open('addressbook.json') as file:
            db_contacts = json.load(file)
        if con.book in db_contacts:
            book = db_contacts.get(con.book)
            if book.get(con.f_name):
                raise Exception("Contact already present")
            book.update({con.f_name: con.model_dump()})
            db_contacts.update({con.book: book})
            # print("add data suuus")
        else:
            db_contacts.update({con.book: {con.f_name: con.model_dump()}})
        with open("addressbook.json", 'w') as file:
            json.dump(db_contacts, file, indent=4)
            return {'message': 'Contact Added', 'status': 201, 'data': con.model_dump()}
    except FileNotFoundError:
        response.status_code = 500
        return {'message': 'File not found', 'status': 500}
    except Exception as ex:
        response.status_code = 400
        return {'massage': str(ex), 'status': 400}

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
