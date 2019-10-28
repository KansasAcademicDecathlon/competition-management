import csv
from html import HTML
import logging

from category import Category
from lunch import Lunch
from person import Person
from room import Room
from school import School


STUDENT_ID_STYLE_STRING="text-align:right;"

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

TIME_STYLE_STRING="text-align:right;"


# pylint: disable=invalid-name
def generate_CoachImport(session):
    """
    Generate the CoachImport.csv file
    TeamID,First Name,Last Name,Email,Phone,Extension,Fax,Website
    @param session Session object
    """
    with open("outputs/CoachImport.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        coaches = session.query(Category).filter_by(
            CategoryDescription='Coach').one().people
        for coach in coaches:
            row = [coach.SchoolID, coach.FirstName, coach.LastName,
                   coach.Email, "", "", "", "www"]
            logging.debug(row)
            csvwriter.writerow(row)


def generate_room_schedules(session):
    """
    Generate HTML schedules of Decatheletes per speech room
    @param session Session object
    """
    for room in session.query(Room).filter_by(RoomKind='S').order_by(Room.RoomID):
        markup = HTML()
        head = markup.head
        head.style(TABLE_STYLE_STRING)
        head.title(room.description())
        body = markup.body

        # Room name
        body.p.b.b(room.description())

        # Table of students
        table = body.table

        table_row = table.tr
        table_row.th("Time")
        table_row.th("Student #")
        table_row.th("Name")

        # for speech in sorted(room.speeches, Person.time_sort()):
        for student in session.query(Person).filter_by(SpeechRoomID=room.RoomID).order_by(Person.SpeechTime):
            table_row = table.tr
            table_row.td(student.SpeechTimeFormatted(), style=TIME_STYLE_STRING)
            table_row.td(str(student.StudentID), style=STUDENT_ID_STYLE_STRING)
            table_row.td(student.FullName())

        with open("outputs/"+room.description()+".html", "wb") as rosterfile:
            rosterfile.write(str(markup))


def generate_rosters(session):
    """
    Generate HTML rosters per school
    @param session Session object
    """
    for school in session.query(School).order_by(School.SchoolID):
        # print school.SchoolName
        markup = HTML()
        head = markup.head
        head.style(TABLE_STYLE_STRING)
        head.title(school.SchoolName)
        body = markup.body

        HEADER_STYLE_STRING = "text-align:left;"

        roster_header = body.table(style="margin-left:auto; margin-right:0")
        # See https://stackoverflow.com/questions/6368061/most-common-way-of-writing-a-html-table-with-vertical-headers
        # Team Number
        team_number_row = roster_header.tr
        team_number_row.th("Team Number", style=HEADER_STYLE_STRING)
        team_number_row.td("{:02d}".format(school.SchoolID), style="text-align:right;")

        # School name
        school_name_row = roster_header.tr
        school_name_row.th("School", style=HEADER_STYLE_STRING)
        school_name_row.td(school.SchoolName)

        # List out the coach(es)
        people = session.query(Person).filter_by(
            SchoolID=school.SchoolID).all()
        for person in people:
            if person.Category.CategoryDescription != "Coach":
                continue
            coach_row = roster_header.tr
            coach_row.th("Coach", style=HEADER_STYLE_STRING)
            coach_row.td(person.FullName())

        # Count of students
        count_row = roster_header.tr
        count_row.th("Count", style=HEADER_STYLE_STRING)

        # Insert spacing paragraph
        body.p()

        # Table of students
        table = body.table(klass="students")

        table_row = table.tr(klass="students")
        table_row.th("ID", klass="students")
        table_row.th("Name", klass="students")
        table_row.th("Category", klass="students")
        table_row.th("Speech Room", klass="students")
        table_row.th("Speech Time", klass="students")
        table_row.th("Test Room", klass="students")
        table_row.th("Test Time", klass="students")

        student_count = 0
        students = session.query(Person).filter_by(
            SchoolID=school.SchoolID).order_by(Person.StudentID).all()
        for student in students:
            # All participating students will have a valid StudentID
            if student.StudentID is None:
                continue
            student_count += 1
            table_row = table.tr(klass="students")
            table_row.td(str(student.StudentID), klass="students", style=STUDENT_ID_STYLE_STRING)
            table_row.td(student.FullName(), klass="students")
            table_row.td(student.Category.CategoryDescription, klass="students")
            table_row.td(student.SpeechRoom.description(), klass="students")
            table_row.td(student.SpeechTimeFormatted(), klass="students", style=TIME_STYLE_STRING)
            table_row.td(student.TestingRoom.description(), klass="students")
            table_row.td(student.TestingTimeFormatted(), klass="students", style=TIME_STYLE_STRING)

        count_row.td(str(student_count), style="text-align:right;")

        if student_count > 0:
            with open("outputs/"+school.SchoolName+".html", "wb") as rosterfile:
                rosterfile.write(str(markup))
        # print school.people


# pylint: disable=invalid-name
def generate_StudentRooms(session):
    """
    Generate the StudentRooms.csv file
    Student Number,Team Number,First Name,Last Name,Speech Room,\
        Speech Time,Interview Room,Interview Time,Testing Room,\
        Test Seat,Essay Room,HSV,Grade,Transcript,Permission,\
        CodeofConduct,ActivityForm
    @param session Session object
    """
    with open("outputs/StudentRooms.csv", "wb") as csvfile:
        csvwriter = csv.writer(csvfile)

        students = session.query(Person).order_by(Person.StudentID).all()
        for student in students:
            if not student.is_student():
                continue

            row = [student.StudentID,
                   student.SchoolID,
                   student.FirstName,
                   student.LastName,
                   student.SpeechRoom.Name,  # Speech Room
                   student.SpeechTime,  # Speech Time
                   student.SpeechRoom.Name,  # Interview Room
                   student.SpeechTime,  # Interview Time
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


# pylint: disable=invalid-name
def generate_TeamImportData(session):
    """
    Generate the TeamImportData.csv file
    Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
        Category,Region
    @param session Session object
    """
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


def generate_totals(session):
    """
    Report the following totals:
    * Teams
    * Decathletes
    * Volunteers
    * Lunches
        * Total per type
        * Grand Total
    @param session Session object
    """
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
    for lunch_choice in lunch_choices:
        print "{0:8} {1}".format(lunch_choice.LunchDescription, lunch_counts[lunch_choice.LunchID])
        lunch_total += lunch_counts[lunch_choice.LunchID]
    print "{0:8} {1}".format("Total", lunch_total)


def generate_volunteer_list(session):
    """
    Generate a list of volunteers
    @param session Session object
    """
    markup = HTML()
    head = markup.head
    head.style(TABLE_STYLE_STRING)
    head.title("Volunteers")
    body = markup.body

    body.p.b("Volunteers")

    # Table of volunteers
    table = body.table

    table_row = table.tr
    table_row.th("School")
    table_row.th("Name")
    table_row.th("Lunch")
    table_row.th("Time")
    table_row.th("Morning Assignment")
    table_row.th("Afternoon Assignment")

    volunteers = session.query(Category).filter_by(
        CategoryDescription='Volunteer').one().people

    for volunteer in volunteers:
        table_row = table.tr
        table_row.td(volunteer.School.SchoolName)
        table_row.td(volunteer.FullName())
        table_row.td(volunteer.Lunch.LunchDescription)
        table_row.td(volunteer.VolunteerTime)
        table_row.td(" ")  # Leave a blank for manually filling in assigment
        assignment_string = " "
        if volunteer.VolunteerTime == "Morning":
            assignment_string = "------------------"
        table_row.td.center(assignment_string)

    with open("outputs/volunteers.html", "wb") as rosterfile:
        rosterfile.write(str(markup))
