from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Site(Base):
    __tablename__ = 'sites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    url = Column(String)
    xpath = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()