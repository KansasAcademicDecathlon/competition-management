import csv
import distutils.dir_util
import logging
from category import Category
from lunch import Lunch
from person import Person
from room import Room
from school import School

from html import HTML

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
    distutils.dir_util.mkpath("outputs")
    with open("outputs/CoachImport.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        coaches = session.query(Category).filter_by(
            CategoryDescription='Coach').one().people
        for coach in coaches:
            row = [coach.SchoolID, coach.FirstName, coach.LastName,
                   coach.Email, "", "", "", "www"]
            logging.debug(row)
            csvwriter.writerow(row)


def generate_room_schedules():
    """
    Generate HTML schedules of Decatheletes per speech room
    """
    Session = sessionmaker(bind=engine)

    session = Session()
    distutils.dir_util.mkpath("outputs")

    for room in session.query(Room).filter_by(RoomKind='S').order_by(Room.RoomID):
        title = "{0} {1}".format(room.Building, room.Name)

        markup = HTML()
        head = markup.head
        # See https://www.w3schools.com/css/tryit.asp?filename=trycss_table_striped for an example of a striped table
        head.style(
            """
            table, th, td {
                border: 2px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: left;
            }
            tr:nth-child(even) {background-color: #f2f2f2;}""")
        head.title(title)
        body = markup.body

        # School name
        p = body.p
        p.b(title)

        # Table of students
        table = body.table

        table_row = table.tr
        table_row.th("Time")
        table_row.th("Student #")
        table_row.th("Name")

        # for speech in sorted(room.speeches, Person.time_sort()):
        for student in session.query(Person).filter_by(SpeechRoomID=room.RoomID).order_by(Person.SpeechRoomTime):
            table_row = table.tr
            table_row.td(str(student.SpeechRoomTime))
            table_row.td(str(student.StudentID))
            table_row.td(student.FullName())

        with open("outputs/"+title+".html", "wb") as rosterfile:
            rosterfile.write(str(markup))


def generate_rosters():
    """
    Generate HTML rosters per school
    """
    Session = sessionmaker(bind=engine)

    session = Session()
    distutils.dir_util.mkpath("outputs")

    for school in session.query(School).order_by(School.SchoolID):
        # print school.SchoolName
        markup = HTML()
        head = markup.head
        # See https://www.w3schools.com/css/tryit.asp?filename=trycss_table_striped for an example of a striped table
        head.style(
            """
            table, th, td {
                border: 2px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: left;
            }
            tr:nth-child(even) {background-color: #f2f2f2;}""")
        head.title(school.SchoolName)
        body = markup.body

        # Team Number
        p = body.p
        p.b("Team Number ")
        p += "{:02d}".format(school.SchoolID)

        # School name
        p = body.p
        p.b("School ")
        p += school.SchoolName

        # List out the coach(es)
        people = session.query(Person).filter_by(
            SchoolID=school.SchoolID).all()
        for person in people:
            if person.Category.CategoryDescription != "Coach":
                continue
            p = body.p
            p.b("Coach ")
            p += person.FullName()

        # Table of students
        table = body.table

        table_row = table.tr
        table_row.th("Student #")
        table_row.th("Name")
        table_row.th("Category")

        students = session.query(Person).filter_by(
            SchoolID=school.SchoolID).order_by(Person.StudentID).all()
        for student in students:
            # All participating students will have a valid StudentID
            if student.StudentID == None:
                continue
            table_row = table.tr
            table_row.td(str(student.StudentID))
            table_row.td(student.FullName())
            table_row.td(student.Category.CategoryDescription)

        with open("outputs/"+school.SchoolName+".html", "wb") as rosterfile:
            rosterfile.write(str(markup))
        # print school.people


def generate_StudentRooms():
    """
    Generate the StudentRooms.csv file
    Student Number,Team Number,First Name,Last Name,Speech Room,\
        Speech Time,Interview Room,Interview Time,Testing Room,\
        Test Seat,Essay Room,HSV,Grade,Transcript,Permission,\
        CodeofConduct,ActivityForm
    """
    Session = sessionmaker(bind=engine)

    session = Session()
    distutils.dir_util.mkpath("outputs")

    with open("outputs/StudentRooms.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        students = session.query(Person).order_by(Person.StudentID).all()
        for student in students:
            if not student.is_student():
                continue

            row = [student.StudentID, student.SchoolID, student.FirstName, student.LastName,
                   student.SpeechRoom.Name,  # Speech Room
                   student.SpeechRoomTime,  # Speech Time
                   student.SpeechRoom.Name,  # Interview Room
                   student.SpeechRoomTime,  # Interview Time
                   student.TestingRoom.Name,  # Testing Room
                   "1",  # Testing Seat
                   "EssayRoomA",  # Essay Room
                   student.CategoryID,
                   "9",  # Grade
                   "False",  # Transcript
                   "False",  # Permission
                   "False",  # CodeofConduct
                   "False"  # ActivityForm
                   ]
            csvwriter.writerow(row)


def generate_TeamImportData():
    """
    Generate the TeamImportData.csv file
    Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
        Category,Region
    """
    Session = sessionmaker(bind=engine)

    session = Session()
    distutils.dir_util.mkpath("outputs")
    with open("outputs/TeamImportData.csv", "wb") as csvfile:
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


def generate_totals():
    """
    Report the following totals:
    * Teams
    * Decathletes
    * Volunteers
    * Lunches
        * Total per type
        * Grand Total
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    lunch_choices = Lunch.lunches(session)
    print lunch_choices

    decathelets = 0
    volunteers = 0
    lunch_counts = {l.LunchID: 0 for l in lunch_choices}

    print lunch_counts

    for school in session.query(School).order_by(School.SchoolID):
        for person in school.people:
            if person.is_student():
                decathelets += 1
                print person
            elif person.Category.CategoryDescription == 'Volunteer':
                volunteers += 1

            lunch_counts[person.LunchID] += 1


    print 'Decathletes {0}'.format(decathelets)
    print 'Volunteers {0}'.format(volunteers)
    print 'Lunches'
    lunch_total = 0
    for l in lunch_choices:
        print "{0:8} {1}".format(l.LunchDescription, lunch_counts[l.LunchID])
        lunch_total += lunch_counts[l.LunchID]
    print "{0:8} {1}".format("Total", lunch_total)


Base.metadata.create_all(engine)

print Category.__table__
print School.__table__
print Person.__table__
