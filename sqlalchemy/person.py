from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class Person(Base):
    __tablename__ = 'Person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    category = relationship("Category")
    #  SchoolID = Column(Integer)
    #  CategoryID = Column(Integer)
    email = Column(String)

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.first_name, self.last_name, self.email)
