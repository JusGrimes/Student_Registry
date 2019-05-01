from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('persons_id', Integer, ForeignKey('persons.id'), primary_key=True),
                          Column('courses_id', Integer, ForeignKey('courses.id'), primary_key=True)
                          )


class Person(Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    enrolled_classes = relationship("Course", secondary=association_table)

    def __repr__(self):
        return f'<Student: id={self.id} first_name={self.first_name}, last_name={self.last_name}>'


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_number = Column(String(4))
    description = Column(String)

    instructor_id = Column(Integer, ForeignKey('persons.id'))
    instructor = relationship('Person')

    enrolled_students = relationship('Person', secondary=association_table, order_by='Person.last_name')

    def __repr__(self):
        return f'<Course: id={self.id} course_number={self.course_number} '\
            f'description={self.description} instructor_id={self.instructor_id}>'

