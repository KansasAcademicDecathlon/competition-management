from sqlalchemy import Column, Integer, String, Time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Person(Base):
    __tablename__ = "Person"

    PersonID = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    CategoryID = Column(Integer, ForeignKey("Category.CategoryID"), nullable=False)
    Category = relationship("Category")
    Lunch = relationship("Lunch")
    LunchID = Column(Integer, ForeignKey("Lunch.LunchID"), nullable=False)
    SchoolID = Column(Integer, ForeignKey("School.SchoolID"))
    School = relationship("School")
    StudentID = Column(String, unique=True)
    Email = Column(String)

    SpeechRoomID = Column(Integer, ForeignKey("Room.RoomID"))
    SpeechTime = Column(Time)
    SpeechRoom = relationship("Room", foreign_keys=[SpeechRoomID])

    TestingRoomID = Column(Integer, ForeignKey("Room.RoomID"))
    TestingRoom = relationship("Room", foreign_keys=[TestingRoomID])
    TestingTime = Column(Time)

    VolunteerTime = Column(String)

    def __repr__(self):
        return "<Person(first='%s', last='%s', email='%s')>" % (
            self.FirstName,
            self.LastName,
            self.Email,
        )

    def FullName(self):
        return "{0} {1}".format(self.FirstName, self.LastName)

    def TestingRoomFormatted(self):
        """
        Return the Testing Room description as a formatted string
        """
        try:
            return self.TestingRoom.description()
        except AttributeError:
            return "????"

    def TestingTimeFormatted(self):
        """
        Return the TestingTime as a formatted string
        """
        try:
            return Person.TimeFormatted(self.TestingTime)
        except AttributeError:
            return "????"

    @staticmethod
    def TimeFormatted(time):
        """
        Return the time object as a formatted string
        """
        # Trick to remove leading zeros in a platform independent way
        # https://stackoverflow.com/a/5900593
        return time.strftime("X%I:%M %p").replace("X0", "X").replace("X", "")

    def SpeechRoomFormatted(self):
        """
        Return the Speech Room description as a formatted string
        """
        try:
            return self.SpeechRoom.description()
        except AttributeError:
            return "????"

    def SpeechTimeFormatted(self):
        """
        Return the SpeechTime as a formatted string
        """
        try:
            return Person.TimeFormatted(self.SpeechTime)
        except AttributeError:
            return "????"

    def is_student(self):
        """
        Is the given person object a student?
        @return True if a student
        """
        return self.StudentID is not None
