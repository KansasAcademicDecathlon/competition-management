from category import Category
from person import Person
from school import School

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from base import Base

engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)

print Category.__table__
print School.__table__
print Person.__table__
