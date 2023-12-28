from sqlalchemy.orm import declarative_base, Session, relationship
from sqlalchemy import Column, String, BigInteger, create_engine, ForeignKey

engine = create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/dbname")
session = Session(engine)
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'book'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)