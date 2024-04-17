#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone."""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Manager for database storage using SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        username = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        cur_env = getenv("HBNB_ENV")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(username, password, host, db),
            pool_pre_ping=True,
        )
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        if cur_env == "test":
            # Base.metadata.drop_all(self.__engine)
            pass

    def all(self, cls=None):
        """Query on the current database session all objects of the given class."""
        if cls is None:
            classes = [Amenity, City, Place, Review, State, User]
            objs = []
            for c in classes:
                # Session should have query method as relaod is always called
                objs += self.__session.query(c).all()
        else:
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        # don't know why it gives me error decralative base should have metadata
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

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

    def close(self):
        """Close the session."""
        self.__session.close()
