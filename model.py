from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import Column, String, BigInteger, create_engine, ForeignKey

engine = create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/book")
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class Book(Base):
    __tablename__ = 'book'

    id = Column(BigInteger, primary_key=True, index=True)
    b_name = Column(String(50), nullable=False, unique=True)
    contact = relationship('Contact',back_populates='book')

    def __repr__(self):
        return self.b_name


class Contact(Base):
    __tablename__ = 'contact'

    id = Column(BigInteger, primary_key=True, index=True)
    f_name = Column(String(50), nullable=False, unique=True)
    l_name = Column(String(50))
    email = Column(String(50),nullable=False)
    phone = Column(BigInteger)
    location = Column(String(100))
    book_id = Column(BigInteger,ForeignKey('book.id',ondelete='CASCADE'),nullable=False)
    book = relationship('Book',back_populates='contact')

    def __repr__(self):
        return self.f_name