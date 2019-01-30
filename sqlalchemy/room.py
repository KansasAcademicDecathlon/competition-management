from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class Room(Base):
    __tablename__ = 'Room'

    RoomID = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    Building = Column(String, nullable=False)

    speeches = relationship("Person", foreign_keys="[Person.SpeechRoomID]")

    def __repr__(self):
        return "<Room(building='%s', name='%s')>" % (
            self.Building, self.Name)
