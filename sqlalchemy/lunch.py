from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base

class Lunch(Base):
    __tablename__ = 'Lunch'

    LunchID = Column(Integer, primary_key=True)
    LunchDescription = Column(String, nullable=False)

    @staticmethod
    def lunches(session):
        """
        Get lunch types
        @return an array of Lunch objects
        """
        return session.query(Lunch).order_by(Lunch.LunchID).all()

    def __repr__(self):
        return "<Lunch(description='%s')>" % (
            self.LunchDescription)
