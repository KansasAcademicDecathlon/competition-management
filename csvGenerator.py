import csv
import logging
from pathlib import Path

from itertools import chain, combinations

from category import Category
from lunch import Lunch
from person import Person
from room import Room
from school import School


STUDENT_ID_STYLE_STRING = "text-align:right;"

# See https://www.w3schools.com/css/tryit.asp?filename=trycss_table_striped
# for an example of a striped table
TABLE_STYLE_STRING = """
        table.students,
        th.students,
        td.students {
            border: 2px solid black;
            border-collapse: collapse;
        }

        th.students,
        td.students {
            padding: 5px;
            text-align: left;
        }

        tr.students:nth-child(even) {
            background-color: #f2f2f2;
        }"""

TIME_STYLE_STRING = "text-align:right;"


# pylint: disable=invalid-name
def generate_CoachImport(session, output_directory):
    """
    Generate the CoachImport.csv file
    TeamID,First Name,Last Name,Email,Phone,Extension,Fax,Website
    @param session Session object
    """
    with open(output_directory / Path("CoachImport.csv"), "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        coaches = (
            session.query(Category).filter_by(CategoryDescription="Coach").one().people
        )
        for coach in coaches:
            row = [
                coach.SchoolID,
                coach.FirstName,
                coach.LastName,
                coach.Email,
                "",
                "",
                "",
                "www",
            ]
            logging.debug(row)
            csvwriter.writerow(row)


# pylint: disable=invalid-name
def generate_StudentRooms(session, output_directory):
    """
    Generate the StudentRooms.csv file
    Student Number,Team Number,First Name,Last Name,Speech Room,\
        Speech Time,Interview Room,Interview Time,Testing Room,\
        Test Seat,Essay Room,HSV,Grade,Transcript,Permission,\
        CodeofConduct,ActivityForm
    @param session Session object
    """
    with open(output_directory / Path("StudentRooms.csv"), "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        students = session.query(Person).order_by(Person.StudentID).all()
        for student in students:
            if not student.is_student():
                continue

            row = [
                student.StudentID,
                student.SchoolID,
                student.FirstName,
                student.LastName,
                student.SpeechRoomFormatted(),  # Speech Room
                student.SpeechTimeFormatted(),  # Speech Time
                student.SpeechRoomFormatted(),  # Interview Room
                student.SpeechTimeFormatted(),  # Interview Time
                student.TestingRoomFormatted(),  # Testing Room
                "1",  # Testing Seat
                "EssayRoomA",  # Essay Room
                student.CategoryID,
                "9",  # Grade
                "False",  # Transcript
                "False",  # Permission
                "False",  # CodeofConduct
                "False",  # ActivityForm
            ]
            csvwriter.writerow(row)


# pylint: disable=invalid-name
def generate_TeamImportData(session, output_directory):
    """
    Generate the TeamImportData.csv file
    Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
        Category,Region
    @param session Session object
    """
    with open(
        output_directory / Path("TeamImportData.csv"), "w", newline=""
    ) as csvfile:
        csvwriter = csv.writer(csvfile)

        for school in session.query(School).order_by(School.SchoolID):
            row = [
                school.SchoolID,
                school.SchoolName,
                school.Address1,
                school.Address2,
                school.City,
                school.State,
                school.ZipCode,
                "MEDIUM",  # Division
                "MEDIUM",  # Category
                "Kansas",  # Region
            ]
            logging.debug(row)
            csvwriter.writerow(row)
