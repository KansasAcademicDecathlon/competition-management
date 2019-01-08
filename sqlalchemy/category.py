from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'Category'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    people = relationship("Person")

    def __repr__(self):
        return "<Category(description='%s')>" % (
            self.description)
