from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class School(Base):
    __tablename__ = 'School'

    SchoolID = Column(Integer, primary_key=True)
    SchoolName = Column(String, nullable=False)
    Address1 = Column(String, nullable=False)
    Address2 = Column(String)
    City = Column(String, nullable=False)
    State = Column(String, nullable=False)
    ZipCode = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
    category = relationship("Category")
    #  SchoolID = Column(Integer)
    #  CategoryID = Column(Integer)
    email = Column(String)

    def __repr__(self):
        return "<User(first='%s', last='%s', email='%s')>" % (
            self.first_name, self.last_name, self.email)
