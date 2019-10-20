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
    Lunch = relationship("Lunch")
    LunchID = Column(Integer, ForeignKey('Lunch.LunchID'), nullable=False)
    SchoolID = Column(Integer, ForeignKey('School.SchoolID'))
    School = relationship("School")
    StudentID = Column(Integer, unique=True)
    Email = Column(String)

    SpeechRoomID = Column(Integer, ForeignKey('Room.RoomID'))
    SpeechTime = Column(Time)
    SpeechRoom = relationship("Room", foreign_keys=[SpeechRoomID])

    TestingRoomID = Column(Integer, ForeignKey('Room.RoomID'))
    TestingRoom = relationship("Room", foreign_keys=[TestingRoomID])
    TestingTime = Column(Time)

    VolunteerTime = Column(String)

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.FirstName, self.LastName, self.Email)

    def FullName(self):
        return "{0} {1}".format(self.FirstName, self.LastName)

    def TestingTimeFormatted(self):
        """
        Return the TestingTime as a formatted string
        """
        return self.TestingTime.strftime("%H:%M")

    def SpeechTimeFormatted(self):
        """
        Return the SpeechTime as a formatted string
        """
        return self.SpeechTime.strftime("%H:%M")

    def is_student(self):
        """
        Is the given person object a student?
        @return True if a student
        """
        return self.StudentID is not None
