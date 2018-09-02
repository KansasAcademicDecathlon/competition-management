/* How to get the list of coaches and their schools
https://www.w3schools.com/sql/sql_join_inner.asp */
/* Old: Select School.SchoolName, Person.FirstName, Person.LastName from Coach inner join Person on Coach.PersonID=Person.PersonID inner join School on Person.SchooID=School.SchoolID */
Select School.SchoolName, Person.FirstName, Person.LastName from Person join School on School.SchoolID=Person.SchooID where Person.CategoryID=4

/* How to get a list of students for a schools */

/* List of all students with school, name and category */
Select School.SchoolName, Person.FirstName, Person.LastName, Category.CategoryDescription from Person join School on School.SchoolID=Person.SchooID join Category on Category.CategoryID=Person.CategoryID where Person.CategoryID in(1,2,3)