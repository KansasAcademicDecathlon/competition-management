import csv
import logging
import os.path
import sqlite3


class Contest(object):
    """ Contest database class """

    def __init__(self):
        self.conn = None

    def __create_tables(self):
        """
        Populate the database with default tables
        """
        logging.debug("Creating default tables")
        self.conn.executescript(
            """
            BEGIN TRANSACTION;
            DROP TABLE IF EXISTS `Category`;
            CREATE TABLE IF NOT EXISTS `Category` (
                `CategoryID`            integer PRIMARY KEY,
                'CategoryDescription'   text
            );
            INSERT INTO 'Category' VALUES (1,'HONORS');
            INSERT INTO 'Category' VALUES (2,'SCHOLASTIC');
            INSERT INTO 'Category' VALUES (3,'VARSITY');
            INSERT INTO 'Category' VALUES (4,'Coach');
            INSERT INTO 'Category' VALUES (5,'Volunteer');

            DROP TABLE IF EXISTS `TestingAppointment`;
            CREATE TABLE IF NOT EXISTS `TestingAppointment` (
                `AppointmentID`	integer PRIMARY KEY,
                `RoomID`	    integer NOT NULL,
                `TestTime`	    datetime NOT NULL
            );
            DROP TABLE IF EXISTS `School`;
            CREATE TABLE IF NOT EXISTS `School` (
                `SchoolID`	    integer PRIMARY KEY,
                `SchoolName`    text NOT NULL,
                `Address1`      text NOT NULL,
                `Address2`      text,
                `City`          text NOT NULL,
                `State`         text NOT NULL,
                `ZipCode`       integer NOT NULL
            );
            DROP TABLE IF EXISTS `Room`;
            CREATE TABLE IF NOT EXISTS `Room` (
                `RoomID`	integer PRIMARY KEY,
                `RoomName`	text NOT NULL
            );
            DROP TABLE IF EXISTS `Person`;
            CREATE TABLE IF NOT EXISTS `Person` (
                `PersonID`	    integer PRIMARY KEY,
                `FirstName`	    text NOT NULL,
                `LastName`	    text NOT NULL,
                'SchoolID'      integer,
                `CategoryID`    integer NOT NULL,
                `Email`	        text
            );
            DROP TABLE IF EXISTS `Decathlete`;
            CREATE TABLE IF NOT EXISTS `Decathlete` (
                `PersonID`	            integer,
                `SpeechAppointment`	    integer,
                `ObjectiveAppointment`	integer
            );
            COMMIT;
            """
        )

    def open_database(self, database_name):
        """
        Open a connection to the database. If the database does not exist,
        create it and populate it with the default tables
        """
        logging.debug("Opening database %s", database_name)

        create_database = False  # Assume the database exists

        if not os.path.isfile(database_name):
            logging.debug("Database does not exist")
            create_database = True

        self.conn = sqlite3.connect(database_name)
        # Use the row factory to allow dictionary style access to the result
        self.conn.row_factory = sqlite3.Row

        if create_database:
            self.__create_tables()

    def schools(self):
        """
        Return a dictionary of SchoolName by SchoolID
        """
        school_dict = {}
        for school in self.conn.execute("SELECT * FROM School"):
            school_dict[school["SchoolID"]] = school["SchoolName"]
        return school_dict

    def coaches_by_school(self, school_id):
        """
        Return a dictionary of coaches by ther IDs for a given school
        """
        coach_dict = {}
        query_string = """Select Person.PersonID, Person.FirstName,
                        Person.LastName from Person
                        where Person.CategoryID=4 AND Person.SchoolID=?"""

        for coach in self.conn.execute(query_string, (school_id,)):
            coach_dict[coach["PersonID"]] = " ".join(
                [coach["FirstName"], coach["LastName"]])

        return coach_dict

    def person_query(self, person_id):
        """
        Return a dictionary for the given person
        """
        query_string = """Select * from Person
                        join Category on Category.CategoryID=Person.CategoryID
                        where Person.PersonID=?"""

        return self.conn.execute(query_string, (person_id,)).fetchone()

    def students_by_school(self, school_id):
        """
        Return a list of students IDs for a given school
        """
        query_string = """Select Person.PersonID from Person
                        where Person.CategoryID in(1,2,3)
                            AND Person.SchoolID=?"""

        # Transform the results into a list of IDs
        return [i[0] for i in self.conn.execute(query_string, (school_id,))]

    def generate_CoachImport(self):
        """
        Generate the CoachImport.csv file
        TeamID,First Name,Last Name,Email,Phone,Extension,Fax,Website
        """
        query_string = """Select SchoolID, FirstName, LastName from Person
                        where Person.CategoryID=4"""

        with open("CoachImport.csv", "wb") as csvfile:
            csvwriter = csv.writer(csvfile)

            for coach in self.conn.execute(query_string):
                row = [coach['SchoolID']]
                row.append(coach['FirstName'])
                row.append(coach['LastName'])
                for _ in range(5):
                    row.append([''])
                logging.debug(row)
                csvwriter.writerow(row)

    def generate_TeamImportData(self):
        """
        Generate the TeamImportData.csv file
        Number,School Name,Address1,Address2,City,State,Zip Code,Division,\
            Category,Region
        """
        fieldnames = ['SchoolID', 'SchoolName',
                      'Address1', 'Address2',
                      'City', 'State', 'ZipCode']

        with open("TeamImportData.csv", "wb") as csvfile:
            csvwriter = csv.writer(csvfile)

            for school in self.conn.execute("SELECT * FROM School"):
                # Pull the revelent fields from the query result for output
                # TODO add handling for filedname is not present
                row = []
                # row = [school[i] for i in fieldnames]
                for i in fieldnames:
                    if i in school.keys():
                        logging.debug(": ".join([i, str(school[i])]))
                        row.append(school[i])
                    else:
                        logging.debug(i + " not present")
                        row.append("")
                logging.debug(row)
                csvwriter.writerow(row)

    def generate_roster_csv(self):
        """
        Generate the Roster Report in CSV format
        """
        fieldnames = ['PersonID', 'FirstName',
                      'LastName', 'CategoryDescription']
        header_names = ['Student #', 'First Name', 'Last Name', 'Category']

        for schoolID, schoolName in self.schools().items():
            logging.debug("Processing School %s", schoolName)
            students = self.students_by_school(schoolID)

            # Skip any schools without students
            if not students:
                logging.debug("No students")
                continue

            logging.debug(students)
            # Create a CSV report for each school
            with open(schoolName + ".csv", "wb") as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write the team number
                csvwriter.writerow(['Team Number', schoolID])
                csvwriter.writerow(['School', schoolName])

                for coach_name \
                        in self.coaches_by_school(schoolID).itervalues():
                    csvwriter.writerow(['Coach', coach_name])

                # Do not use writeheader as it does not match the dictionary
                # names
                csvwriter.writerow(header_names)

                # Query the database for the list of students in that school
                for student in students:
                    # Obtain the student information from the database
                    student = self.person_query(student)
                    # Pull the revelent fields from the query result for output
                    row = [student[i] for i in fieldnames]
                    logging.debug(row)
                    csvwriter.writerow(row)
