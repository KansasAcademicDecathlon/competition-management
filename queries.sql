/* How to get the list of coaches and their schools
https://www.w3schools.com/sql/sql_join_inner.asp */
Select School.SchoolName, Person.FirstName, Person.LastName from Person
join School on School.SchoolID=Person.SchoolID
where Person.CategoryID=4;

/* How to get a list of students for a schools */
Select School.SchoolName, Person.FirstName, Person.LastName, Category.CategoryDescription from Person
join School on School.SchoolID=Person.SchoolID
join Category on Category.CategoryID=Person.CategoryID
where Person.CategoryID in(1,2,3) AND Person.SchoolID=3;

/* List of all students with school, name and category */
Select School.SchoolName, Person.FirstName, Person.LastName, Category.CategoryDescription from Person
join School on School.SchoolID=Person.SchoolID
join Category on Category.CategoryID=Person.CategoryID
where Person.CategoryID in(1,2,3);