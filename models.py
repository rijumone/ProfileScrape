import os
import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini'))

import datetime
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, DECIMAL, DateTime

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
    x_coord = Column(Integer)
    y_coord = Column(Integer)
    
    def __repr__(self):
        return '''<Source (
                    name={name},
                    x_coord={x_coord},
                    y_coord={y_coord},
                    )>'''.format(
                        name=self.name,
                        x_coord=self.x_coord,
                        y_coord=self.y_coord,
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
    profile_id = Column(Integer)
    uuid = Column(String)

    def __repr__(self):
        return '''<Picture (
                    id={id},     
                    uuid={uuid},     
                )>'''.format(
                    id=self.id,
                    uuid=self.uuid,
                )

class User(Base):
    __tablename__ = 'user'
    
    name = Column(String, primary_key=True)
    
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
