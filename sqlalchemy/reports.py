import csv
import logging
from category import Category
from person import Person
from school import School

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base

engine = create_engine('sqlite:///:memory:', echo=True)


def generate_CoachImport():
    """
    Generate the CoachImport.csv file
    TeamID,First Name,Last Name,Email,Phone,Extension,Fax,Website
    """

    Session = sessionmaker(bind=engine)

    session = Session()

    with open("CoachImport.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        coaches = session.query(Category).filter_by(
            CategoryDescription='Coach').one().people
        for coach in coaches:
            row = [coach.SchoolID, coach.FirstName, coach.LastName,
                   coach.Email, "", "", "", "www"]
            logging.debug(row)
            csvwriter.writerow(row)


def generate_TeamImportData():
    """
    Generate the TeamImportData.csv file
    Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
        Category,Region
    """
    Session = sessionmaker(bind=engine)

    session = Session()
    with open("TeamImportData.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        for school in session.query(School).order_by(School.SchoolID):
            row = [school.SchoolID, school.SchoolName, school.Address1,
                   school.Address2, school.City, school.State, school.ZipCode,
                   "MEDIUM",  # Division
                   "MEDIUM",  # Category
                   "Kansas"   # Region
                   ]
            logging.debug(row)
            csvwriter.writerow(row)

Base.metadata.create_all(engine)

print Category.__table__
print School.__table__
print Person.__table__
