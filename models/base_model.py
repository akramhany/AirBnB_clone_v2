#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone."""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models."""

    def __init__(self, *args, **kwargs):
        """Instatntiate a new model."""
        if not kwargs:
            from models import storage

            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            kwargs["updated_at"] = datetime.strptime(
                kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            kwargs["created_at"] = datetime.strptime(
                kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            del kwargs["__class__"]
            self.__dict__.update(kwargs)

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
        from models import storage

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary
