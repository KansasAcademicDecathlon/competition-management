from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Person(Base):
    __tablename__ = 'Person'

    PersonID = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    CategoryID = Column(Integer, ForeignKey('Category.id'), nullable=False)
    Category = relationship("Category")
    SchoolID = Column(Integer)
    School = relationship("School")
    Email = Column(String)

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.first_name, self.last_name, self.email)
