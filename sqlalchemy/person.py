from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Person(Base):
    __tablename__ = 'Person'

    PersonID = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    CategoryID = Column(Integer, ForeignKey('Category.CategoryID'), nullable=False)
    Category = relationship("Category")
    SchoolID = Column(Integer, ForeignKey('School.SchoolID'))
    School = relationship("School")
    Email = Column(String)

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.FirstName, self.LastName, self.Email)
