#!/usr/bin/python3
"""This module defines a class User."""
from sqlalchemy import Column, String

import models
from models.base_model import BaseModel


class User(BaseModel):
    """This class defines a user by various attributes."""

    if models.storage_type == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
