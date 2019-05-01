from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Models.schema import Person, Base, Course
from UserInterface import UserInterface
from registry import Registry

if __name__ == '__main__':
    dbURL = "sqlite:///blarg.db"

    engine = create_engine(dbURL, echo=False)
    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    registry = Registry(session)

    ui = UserInterface(registry)

    ui.run()
    session.close()

