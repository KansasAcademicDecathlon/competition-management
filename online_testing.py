import csv
import logging

from itertools import chain, combinations

from category import Category
from person import Person
from room import Room
from school import School

logger = logging.getLogger(__name__)


def generate_SchoolInformationFile(session):
    """
    Generate a CSV School Information File for import into the USAD online testing system
    domain,school's name,school's contact - first name,school's contact - last name,school's city,state director's USAD state code for the school
    @param session Session object
    """
    with open("outputs/SchoolInformationFile.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)

        for school in session.query(School).order_by(School.SchoolID):
            # Use the join to be able to filter by CategoryDescription
            # Assume the first coach is the contact
            coach = (
                session.query(Person)
                .join(Person.Category)
                .filter(Person.SchoolID == school.SchoolID)
                .filter(Category.CategoryDescription == "Coach")
                .first()
            )

            if not coach:
                logger.error("%s is missing a coach!", school.SchoolName)
                continue

            row = [
                # Must include the @ sign
                "@" + school.Domain,
                school.SchoolName,
                coach.FirstName,
                coach.LastName,
                school.City,
                school.State,
            ]
            logging.debug(row)
            csvwriter.writerow(row)


def generate_StudentTeamInformationFile(session):
    """
    Generate a CSV Student Team Information File for import into the USAD online testing system
    student ID,domain,First Name,Last Name,Division (HSV)
    @param session Session object
    """
    with open("outputs/StudentTeamInformationFile.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)

        for student in (
            session.query(Person)
            .join(Person.Category)
            .filter(Category.get_student_filter())
        ):
            row = [
                student.StudentID,
                "@" + student.School.Domain,
                student.FirstName,
                student.LastName,
                student.Category.CategoryDescription[0],
            ]
            logging.debug(row)
            csvwriter.writerow(row)
