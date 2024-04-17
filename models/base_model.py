#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

import models
from models import storage

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiate a new model."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, val in kwargs.items():
                if key != "__class__":
                    setattr(self, key, val)

            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            else:
                self.id = kwargs.get("id")
            if kwargs.get("created_at", None) is None:
                self.created_at = datetime.now()
            else:
                self.created_at = datetime.strptime(
                    kwargs.get("created_at", None), "%Y-%m-%dT%H:%M:%S.%f"
                )
            if kwargs.get("updated_at", None) is None:
                self.updated_at = datetime.now()
            else:
                self.updated_at = datetime.strptime(
                    kwargs.get("updated_at", None), "%Y-%m-%dT%H:%M:%S.%f"
                )

    def add_attr(self, attr_name, attr_value):
        """Take an attribute name and a value and updates it."""
        try:
            if attr_value[0] == '"' and attr_value[-1] == '"':
                st = attr_value.strip('"')
                argu = ""
                sp = ""
                for word in st.split("_"):
                    word = sp + word
                    argu += word
                    sp = " "
                self.__dict__[attr_name] = argu
            elif "." in attr_value:
                self.__dict__[attr_name] = float(attr_value)
            else:
                self.__dict__[attr_name] = int(attr_value)
        except KeyError:
            self.__dict__[attr_name] = str(attr_value)

    def __str__(self):
        """Return a string representation of the instance."""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Update updated_at with current time when instance is changed."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
