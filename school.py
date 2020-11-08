from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class School(Base):
    __tablename__ = "School"

    SchoolID = Column(Integer, primary_key=True)
    SchoolName = Column(String, nullable=False)
    Address1 = Column(String, nullable=False)
    Address2 = Column(String)
    City = Column(String, nullable=False)
    State = Column(String, nullable=False)
    ZipCode = Column(String, nullable=False)

    people = relationship("Person")

    def __repr__(self):
        return "<User(first='%s', last='%s', email='%s')>" % (
            self.first_name,
            self.last_name,
            self.email,
        )
