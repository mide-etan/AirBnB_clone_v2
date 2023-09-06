#!/usr/bin/python3
"""the DBStorage engine."""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self._extracted_from_all_10()
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {f"{type(o).__name__}.{o.id}": o for o in objs}

    # TODO Rename this here and in `all`
    def _extracted_from_all_10(self):
        result = self.__session.query(State).all()
        result.extend(self.__session.query(City).all())
        result.extend(self.__session.query(User).all())
        result.extend(self.__session.query(Place).all())
        result.extend(self.__session.query(Review).all())
        result.extend(self.__session.query(Amenity).all())
        return result

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        session = scoped_session(session_factory)
        self.__session = session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
