from sqlalchemy import create_engine,Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker,declarative_base
from os import environ

DATABASE_URL = environ.get('DATABASE_URL', 'sqlite:///./addresses.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)