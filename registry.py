from typing import List

from sqlalchemy.orm import Session

from Models.schema import Person, Course


class Registry():

    def __init__(self, session: Session):
        self.session = session

    def close(self):
        self.session.close()

    def addPerson(self, firstname: str, lastname: str):
        newPerson = Person(first_name=firstname, last_name=lastname)

        self.session.add(newPerson)
        self.session.commit()

    def _addPersons(self, people: List[Person]):
        self.session.add_all(people)

        self.session.commit()

    def removePersons(self, people: List[Person]):
        for person in people:
            self.session.delete(person)
        self.session.commit()

    def listPersons(self):
        return self.session.query(Person)

    def getPerson(self, studentID) -> Person:
        return self.session.query(Person).filter(Person.id == studentID).one_or_none()

    def addPersonToCourseByID(self, student_id, course_id):
        student = self.session.query(Person).filter(Person.id == student_id).one_or_none()
        course = self.session.query(Course).filter(Course.id == course_id).one_or_none()

        if student is None:
            raise LookupError('Student was not found')
        if course is None:
            raise LookupError('Course was not found')

        student.enrolled_classes.append(course)

    def addCourse(self, course_number, course_desc):

        course = Course(course_number=course_number,description=course_desc)

        self.session.add(course)
        self.session.commit()

    def listCourses(self):
        return self.session.query(Course)

    def getCourse(self, course_id):
        return self.session.query(Course).filter(Course.id == course_id).one_or_none()

    def removeCourse(self, course_id):
        course = self.session.query(Course).filter(Course.id == course_id).one_or_none()
        self.session.delete(course)
        self.session.commit()

    def removePerson(self, student_id):
        person = self.session.query(Person).filter(Person.id == student_id).one_or_none()
        self.session.delete(person)
        self.session.commit()

