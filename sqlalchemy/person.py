from sqlalchemy import Column, Integer, String, Time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Person(Base):
    __tablename__ = 'Person'

    PersonID = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    CategoryID = Column(Integer, ForeignKey(
        'Category.CategoryID'), nullable=False)
    Category = relationship("Category")
    LunchID = Column(Integer, ForeignKey('Lunch.LunchID'), nullable=False)
    SchoolID = Column(Integer, ForeignKey('School.SchoolID'))
    School = relationship("School")
    StudentID = Column(Integer, unique=True)
    Email = Column(String)

    SpeechRoomID = Column(Integer, ForeignKey('Room.RoomID'))
    SpeechRoomTime = Column(Time)
    SpeechRoom = relationship("Room", foreign_keys=[SpeechRoomID])

    TestingRoomID = Column(Integer, ForeignKey('Room.RoomID'))
    TestingRoom = relationship("Room", foreign_keys=[TestingRoomID])

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.FirstName, self.LastName, self.Email)

    def FullName(self):
        return "{0} {1}".format(self.FirstName, self.LastName)

    def is_student(self):
        """
        Is the given person object a student?
        @return True if a student
        """
        return self.StudentID != None
