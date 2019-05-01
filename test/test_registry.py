from typing import List

import pytest
from pytest import fail
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Models.schema import Base, Person
from registry import Registry


class TestRegistry():

    @pytest.fixture
    def db_session(self) -> Session:
        url = "sqlite:///:memory:"
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        session = Session(bind=engine)

        return session

    @pytest.fixture
    def register(self, db_session):
        reg = Registry(db_session)
        yield reg
        reg.close()

    @pytest.mark.parametrize('people', [
        [Person(first_name='John', last_name='Doe')],
        [Person(first_name='John', last_name='Doe'),
         Person(first_name='John', last_name='Doe')],

    ])
    def test_add_people_to_db(self, db_session, register, people: List[Person]):
        register._addPersons(people)

        for person in people:
            if person not in db_session:
                assert fail()
        assert True

    def test_no_duplicate_people(self, db_session, register):
        person = Person(first_name='John', last_name='Doe')

        register._addPersons([person])
        register._addPersons([person])

        assert db_session.query(Person).count() == 1

    def test_add_then_remove_person_verify_not_in_DB(self, db_session, register):
        person = Person(first_name='John', last_name='Doe')

        register._addPersons([person])
        register.removePersons([person])

        assert person not in db_session

    @pytest.mark.parametrize('people',[
        [Person(first_name='John', last_name='Doe')]
    ])
    def test_remove_person_from_db(self, db_session, register, people):
        register._addPersons(people)

        register.removePersons(people)

        for person in people:
            if person in db_session:
                fail()
        assert True
