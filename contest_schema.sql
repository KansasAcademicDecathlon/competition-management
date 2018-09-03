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
	`SchoolName`    text NOT NULL
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
