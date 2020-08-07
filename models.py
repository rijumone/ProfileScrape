import os
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini'))

import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, DECIMAL, DateTime, Boolean

Base = declarative_base()
engine = create_engine(
    'mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{db}'.format(
        user=config['DATABASE']['username'],
        pw=config['DATABASE']['password'],
        host=config['DATABASE']['host'],
        db=config['DATABASE']['database'],
        port=config['DATABASE']['port'],
        ), 
    echo=False
    )
Session = sessionmaker(bind=engine)
session = Session()

class Source(Base):
    __tablename__ = 'source'

    name = Column(String, primary_key=True)
    call_order = Column(Integer)
    is_active = Column(Boolean)
    
    def __repr__(self):
        return '''<Source (
                    name={name},
                    )>'''.format(
                        name=self.name,
                    )

class Region(Base):
    __tablename__ = 'region'

    name = Column(String, primary_key=True)
    
    def __repr__(self):
        return '''<Region (
                    name={name},
                    )>'''.format(
                        name=self.name,
                    )

class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    bio = Column(String)
    gender = Column(String)
    distance = Column(String)
    locality = Column(String)
    region = Column(String)
    occupation = Column(String)
    sunsign = Column(String)
    last_active = Column(String)
    raw = Column(String)
    result = Column(Boolean, default=True)
    source_name = Column(String)
    
    def __repr__(self):
        return '''<Person (
                    name={name},
                    age={age},
                    )>'''.format(
                        name=self.name,
                        age=self.age,
                    )       

class Picture(Base):
    __tablename__ = 'picture'
    
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer)
    _uuid = Column('uuid', String)

    def __repr__(self):
        return '''<Picture (
                    id={id},     
                    uuid={_uuid},     
                )>'''.format(
                    id=self.id,
                    _uuid=self._uuid,
                )

class User(Base):
    __tablename__ = 'user'
    
    name = Column(String, primary_key=True)
    device_id = Column(String)
    is_active = Column(Boolean)
    screen_resolution_width = Column(Integer)
    screen_resolution_height = Column(Integer)
    
    def __repr__(self):
        return '''<User (
                    name={name},     
                )>'''.format(
                    name=self.name,
                )

class Run(Base):
    __tablename__ = 'run'

    id = Column(Integer, primary_key=True)
    source_name = Column(String)
    user_name = Column(String)
    time_to_sleep = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '''<Run (
                    source_name={source_name},     
                    time_to_sleep={time_to_sleep},     
                )>'''.format(
                    source_name=self.source_name,
                    time_to_sleep=self.time_to_sleep,
                )
