import os

from registry import Registry


class UserInterface():
    _screensize = 100

    def __init__(self, registry: Registry):
        self.registry = registry

    def run(self):
        self.mainMenu()

    def _printHeader(self, title: str):

        full_line = '{:{fillChar}^{screenLength}}'.format('', fillChar='*', screenLength=UserInterface._screensize)
        subject_line = '{title:{fillChar}^{screenLength}}'. \
            format('', fillChar='*', screenLength=UserInterface._screensize, title=' ' + title + ' ')

        os.system('cls')
        print(full_line)
        print(subject_line)
        print(full_line)
        print()

    def _anyKeyToContinue(self):
        input('Press any key to continue')

    def mainMenu(self):

        introText = '\n'
        options = [
            ('Add Student', self.addStudent),
            ('List Students', self.listStudents),
            ('Student Info', self.studentInfo),
            ('Enroll Student', self.enrollStudent),
            ('Add Course', self.addCourse),
            ('List Courses', self.listCourses),
            ('Course Info', self.courseInfo),
            ('Remove Course', self.removeCourse),
            ('Remove Student', self.removeStudent)
        ]

        selection = ''

        while selection != 'quit':
            self._printHeader('Student Registry')
            print(introText)

            for idx, opt in enumerate(options, start=1):
                print(f'{idx}.) {opt[0]}')

            raw_input = input("Select Option (quit to exit): ")
            if raw_input == 'quit':
                break
            try:
                selection = int(raw_input)
            except ValueError as e:
                continue

            if 0 < selection <= len(options):
                options[selection - 1][1]()
                self._anyKeyToContinue()

    def addStudent(self):
        self._printHeader('Add Student')

        introText = 'Please enter the below Unique fields'

        print(introText)
        firstname = input('first name: ')
        lastname = input('last name: ')

        self.registry.addPerson(firstname, lastname)

    def listStudents(self):
        self._printHeader('List of Students')
        print("Current Students:")

        for idx, person in enumerate(self.registry.listPersons(), start=1):
            print(f'{idx:>3}.) {person.first_name} {person.last_name} id={person.id}')

    def studentInfo(self):
        self._printHeader('Student Info')

        while True:
            try:
                id = int(input("Please enter the student's ID"))
            except ValueError as e:
                print('Please enter a number')
                continue

            student = self.registry.getPerson(id)

            if student is None:
                continue

            print(f'{student.first_name} {student.last_name}')
            print('Enrolled Courses: ')

            if not student.enrolled_classes:
                print('None')
            for course in student.enrolled_classes:
                print(f'{course.course_number} {course.description}')

            break

    def enrollStudent(self):
        self._printHeader('Enroll Student')

        while True:
            try:
                course_id = int(input('Course id: '))
                student_id = int(input('Student id: '))
            except ValueError as e:
                print('Please enter an integer value')
                continue
            break

        try:
            self.registry.addPersonToCourseByID(student_id, course_id)
        except LookupError as e:
            print(e)

    def addCourse(self):
        self._printHeader("Add Course")

        course_number = input('Course number: ')
        course_description = input('Course Description: ')

        self.registry.addCourse(course_number, course_description)


    def listCourses(self):
        self._printHeader('List Courses')
        print('All Courses: ')
        for idx, course in enumerate(self.registry.listCourses(),start=1):
            print(f'{idx:>3}.) {course.course_number} {course.description}')

    def courseInfo(self):
        self._printHeader('Course Info')
        while True:
            try:
                course_id = int(input('Enter a course id: '))
            except ValueError as e:
                continue
            course = self.registry.getCourse(course_id)

            if course is None:
                continue
            print(f'{course.course_number} {course.description}')
            break

    def removeCourse(self):
        self._printHeader('Remove Course')
        course_id = None
        while True:
            try:
                course_id = int(input('Enter course id: '))
            except ValueError:
                print('Please enter a number')
                continue
            break
        self.registry.removeCourse(course_id)

    def removeStudent(self):
        self._printHeader('Remove Student')
        student_id = None
        while True:
            try:
                student_id = int(input('Enter student id: '))
            except ValueError:
                print('Please enter a number')
                continue
            break
        self.registry.removePerson(student_id)
