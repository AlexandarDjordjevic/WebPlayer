#!/bin/python 
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import json

engine = create_engine('sqlite:///data.db', echo=False)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Stream(Base):
    __tablename__ = 'streams'
    id = Column(Integer, primary_key=True)
    name = Column('Name', String)
    url = Column('URL', String)
    genre = Column('Genre', String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def create_database_and_tables():
    Base.metadata.create_all(engine)
    session.commit()

def get_stream_list():
    streams = session.query(Stream)
    stream_list = list()
    for stream in streams:
        stream_list.append({ 'name' : stream.name , 'url' : stream.url, 'genre' : stream.genre})
    return json.dumps(stream_list)