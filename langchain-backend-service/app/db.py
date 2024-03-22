from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__="customers"
    id = Column(Integer, primary_key=True)
    name=Column(String)

    def to_json(self):    
        return {"id":self.id, "name":self.name}
    
class Review(Base):
    __tablename__="reviews"
    id=Column(Integer,primary_key=True)
    review=Column(String)

    def to_json(self):
        return {"id": self.id, "review": self.review}
    
engine = create_engine("sqlite:///irm.db")
Session = sessionmaker(bind=engine)