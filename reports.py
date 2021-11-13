import csv
import htmlBuilder
from htmlBuilder.tags import B, Body, Head, Html, Title, P, Table, Td, Th, Tr
from htmlBuilder.attributes import Class, Style
import logging

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
def generate_CoachImport(session):
    """
    Generate the CoachImport.csv file
    TeamID,First Name,Last Name,Email,Phone,Extension,Fax,Website
    @param session Session object
    """
    with open("outputs/CoachImport.csv", "w") as csvfile:
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


def generate_room_schedules(session):
    """
    Generate HTML schedules of Decatheletes per speech room
    @param session Session object
    """
    for room in session.query(Room).filter_by(RoomKind="S").order_by(Room.RoomID):
        students = (
            session.query(Person)
            .filter_by(SpeechRoomID=room.RoomID)
            .order_by(Person.SpeechTime)
        )

        html = Html(
            [],
            Head(
                [],
                htmlBuilder.tags.Style([], TABLE_STYLE_STRING),
                Title([], room.description()),
            ),
            Body(
                [],
                # Room name
                P([], B([], B([], room.description()))),
                Table(
                    [],
                    # Headers
                    Tr([], Th([], "Time"), Th([], "Student #"), Th([], "Name")),
                    # List comprehension to create student rows
                    [
                        Tr(
                            [],
                            Td(
                                [Style(TIME_STYLE_STRING)],
                                student.SpeechTimeFormatted(),
                            ),
                            Td(
                                [Style(STUDENT_ID_STYLE_STRING)],
                                str(student.StudentID),
                            ),
                            Td([], student.FullName()),
                        )
                        for student in students
                    ],
                ),
            ),
        )

        with open("outputs/" + room.description() + ".html", "w") as rosterfile:
            rosterfile.write(html.render())


def generate_rosters(session):
    """
    Generate HTML rosters per school
    @param session Session object
    """

    for school in session.query(School).order_by(School.SchoolID):
        # print(school.SchoolName)
        HEADER_STYLE_STRING = "text-align:left;"

        coaches = (
            session.query(Person)
            .join(Person.Category)
            .filter(Person.SchoolID == school.SchoolID)
            .filter(Category.CategoryDescription == "Coach")
        )

        students = (
            session.query(Person)
            .filter_by(SchoolID=school.SchoolID)
            .filter(Person.SchoolID.isnot(None))
            .order_by(Person.StudentID)
            .all()
        )

        html = Html(
            [],
            Head(
                [],
                htmlBuilder.tags.Style([], TABLE_STYLE_STRING),
                Title([], school.SchoolName + " Roster"),
            ),
            Body(
                [],
                # See https://stackoverflow.com/questions/6368061/most-common-way-of-writing-a-html-table-with-vertical-headers
                Table(
                    [Style("margin-left:auto; margin-right:0")],
                    # Team Number
                    Tr(
                        [],
                        Th([Style(HEADER_STYLE_STRING)], "Team Number"),
                        Td([], "{:02d}".format(school.SchoolID)),
                    ),
                    # School name
                    Tr(
                        [],
                        Th([Style(HEADER_STYLE_STRING)], "School"),
                        Td([], school.SchoolName),
                    ),
                    # List out the coach(es)
                    [
                        Tr(
                            [],
                            Th([Style(HEADER_STYLE_STRING)], "Coach"),
                            Td([], coach.FullName()),
                        )
                        for coach in coaches
                    ],
                    # Count of students
                    Tr(
                        [],
                        Th([Style(HEADER_STYLE_STRING)], "Count"),
                        Td([], str(len(students))),
                    ),
                ),
                # Insert spacing paragraph
                P([]),
                # Table of students
                Table(
                    [Class("students")],
                    Tr(
                        [Class("students")],
                        Th([Class("students")], "ID"),
                        Th([Class("students")], "Name"),
                        Th([Class("students")], "Category"),
                        Th([Class("students")], "Speech Room"),
                        Th([Class("students")], "Speech Time"),
                        Th([Class("students")], "Test Room"),
                        Th([Class("students")], "AM Test Time"),
                        Th([Class("students")], "PM Test Time"),
                    ),
                    # List comprehension to create student rows
                    [
                        Tr(
                            [Class("students")],
                            Td(
                                [Class("students"), Style(STUDENT_ID_STYLE_STRING)],
                                str(student.StudentID),
                            ),
                            Td([Class("students")], student.FullName()),
                            Td(
                                [Class("students")],
                                student.Category.CategoryDescription,
                            ),
                            Td([Class("students")], student.SpeechRoomFormatted()),
                            Td(
                                [Class("students"), Style(TIME_STYLE_STRING)],
                                student.SpeechTimeFormatted(),
                            ),
                            Td([Class("students")], student.TestingRoomFormatted()),
                            Td(
                                [Class("students"), Style(TIME_STYLE_STRING)],
                                student.TestingTimeFormatted(),
                            ),
                            Td(
                                [Class("students"), Style(TIME_STYLE_STRING)], "1:40 PM"
                            ),
                        )
                        for student in students
                    ],
                ),
            ),
        )

        if len(students):
            with open("outputs/" + school.SchoolName + ".html", "w") as rosterfile:
                rosterfile.write(html.render())
        # print(school.people)


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
    with open("outputs/StudentRooms.csv", "w") as csvfile:
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
def generate_TeamImportData(session):
    """
    Generate the TeamImportData.csv file
    Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
        Category,Region
    @param session Session object
    """
    with open("outputs/TeamImportData.csv", "w") as csvfile:
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


def generate_totals(session):
    """
    Report the following totals:
    * Teams
    * Decathletes
        * Count per team
        * Grand Total
    * Volunteers
    * Lunches
        * Total per type
        * Grand Total
    @param session Session object
    """
    lunch_choices = Lunch.lunches(session)
    logging.debug(lunch_choices)

    decathelets = 0
    volunteers = 0
    lunch_counts = {l.LunchID: 0 for l in lunch_choices}
    # decathlete totals for each school. Used for testing room split calculation.
    school_totals = dict()

    logging.debug(lunch_counts)

    for school in session.query(School).order_by(School.SchoolID):
        school_totals[school.SchoolName] = 0
        for person in school.people:
            if person.is_student():
                school_totals[school.SchoolName] += 1
            elif person.Category.CategoryDescription == "Volunteer":
                volunteers += 1

            lunch_counts[person.LunchID] += 1

        decathelets = decathelets + school_totals[school.SchoolName]

        if school_totals[school.SchoolName]:
            print("{}: {}".format(school.SchoolName, school_totals[school.SchoolName]))
        else:
            # Schools without decathletes should be removed from the room split calculation below
            del school_totals[school.SchoolName]

    best_combination = find_room_split(school_totals)

    print("First Testing Session")
    for entry in best_combination:
        print("* {}".format(entry))
    print("Decathletes {}".format(decathelets))
    print("Volunteers {}".format(volunteers))
    print("Lunches")
    lunch_total = 0
    for lunch_choice in lunch_choices:
        print(
            "{:8} {}".format(
                lunch_choice.LunchDescription, lunch_counts[lunch_choice.LunchID]
            )
        )
        lunch_total += lunch_counts[lunch_choice.LunchID]
    print("{:8} {}".format("Total", lunch_total))


def generate_volunteer_list(session):
    """
    Generate a list of volunteers
    @param session Session object
    """
    return
    markup = HTML()
    head = markup.head
    head.style(TABLE_STYLE_STRING)
    head.title("Volunteers")
    body = markup.body

    body.p.b("Volunteers")

    # Table of volunteers
    table = body.table(klass="students")

    table_row = table.tr
    table_row.th("School", klass="students")
    table_row.th("Name", klass="students")
    table_row.th("Lunch", klass="students")
    table_row.th("Time", klass="students")
    table_row.th("Morning Assignment", klass="students")
    table_row.th("Afternoon Assignment", klass="students")

    volunteers = (
        session.query(Category).filter_by(CategoryDescription="Volunteer").one().people
    )

    for volunteer in volunteers:
        table_row = table.tr(klass="students")
        table_row.td(volunteer.School.SchoolName, klass="students")
        table_row.td(volunteer.FullName(), klass="students")
        table_row.td(volunteer.Lunch.LunchDescription, klass="students")
        try:
            volunteer_time_text = volunteer.VolunteerTime
        except AttributeError:
            volunteer_time_text = None

        if not volunteer_time_text:
            volunteer_time_text = "????"

        table_row.td(volunteer_time_text, klass="students")
        # Leave a blank for manually filling in assigment
        table_row.td(" ", klass="students")
        if volunteer.VolunteerTime == "Morning":
            table_row.td(klass="students").hr(style="border-top: 2px dotted black;")
        else:
            # Leave a blank for manually filling in assigment
            table_row.td(" ", klass="students")

    with open("outputs/volunteers.html", "wb") as rosterfile:
        rosterfile.write(str(markup))


def powerset(iterable):
    """
    Compute all the different possible combinations of the given iterable
    See https://docs.python.org/2.7/library/itertools.html#itertools-recipes
    @return iterator
    """
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def find_room_split(counts):
    """
    Find the ideal room split given the different combinations of teams
    @param counts Dictionary of school's number of team members
    @return the optimum list of schools to test together. None if there is no optimum split.
    """
    grand_total = 0

    for entry, value in counts.items():
        grand_total = grand_total + value

    # The optimum is an even split
    optimum_count = grand_total / 2

    # The maximum distance from the optimum is the optimum
    distance_from_optimum = optimum_count

    best_combination = None

    # Compute all the possible combinations of schools using a powerset
    combinations = list(powerset(counts))

    for combination in combinations:
        combination_total = 0
        # Generate the total students for this combination
        for school in combination:
            combination_total = combination_total + counts[school]

        if abs(optimum_count - combination_total) < distance_from_optimum:
            best_combination = combination
            logging.debug("New Best Combination: {}".format(best_combination))
            distance_from_optimum = abs(optimum_count - combination_total)
            logging.debug("Distance {}".format(distance_from_optimum))

    return best_combination
