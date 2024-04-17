#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

import models

if models.storage_type == "db":
    Base = declarative_base()
else:
    Base = object

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """A base class for all hbnb models."""

    if models.storage_type == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiate a new model."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            for key, val in kwargs.items():
                if key != "__class__":
                    setattr(self, key, val)

            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            else:
                self.id = kwargs.get("id")
            if kwargs.get("created_at", None) is None:
                self.created_at = datetime.utcnow()
            else:
                self.created_at = datetime.strptime(
                    kwargs.get("created_at", None), TIME_FORMAT
                )
            if kwargs.get("updated_at", None) is None:
                self.updated_at = datetime.now()
            else:
                self.updated_at = datetime.strptime(
                    kwargs.get("updated_at", None), TIME_FORMAT
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
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """Update updated_at with current time when instance is changed."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(TIME_FORMAT)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(TIME_FORMAT)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)
