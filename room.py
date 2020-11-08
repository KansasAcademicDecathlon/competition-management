from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class Room(Base):
    __tablename__ = "Room"

    RoomID = Column(Integer, primary_key=True)
    Number = Column(String, nullable=False)
    Name = Column(String, nullable=False)
    RoomKind = Column(String, nullable=False)
    speeches = relationship("Person", foreign_keys="[Person.SpeechRoomID]")

    def __repr__(self):
        return "<Room(name='%s' number='%s')>" % (self.Name, self.Number)

    def description(self):
        """
        Name and Number strings combined
        @return concatenated string
        """
        return "{0} {1}".format(self.Name, self.Number)
