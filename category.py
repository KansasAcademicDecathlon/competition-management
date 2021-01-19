import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from base import Base


class Category(Base):
    __tablename__ = "Category"

    CategoryID = Column(Integer, primary_key=True)
    CategoryDescription = Column(String, nullable=False)
    people = relationship("Person")

    def __repr__(self):
        return "<Category(description='%s')>" % (self.CategoryDescription)

    @staticmethod
    def get_student_filter():
        return sqlalchemy.sql.expression.or_(
            Category.CategoryDescription == "HONORS",
            Category.CategoryDescription == "SCHOLASTIC",
            Category.CategoryDescription == "VARSITY",
        )
