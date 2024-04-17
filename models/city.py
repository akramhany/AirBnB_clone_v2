#!/usr/bin/python3
"""City Module for HBNB project."""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


class City(BaseModel):
    """The city class, contains state ID and name."""

    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """Initialize a city."""
        super().__init__(*args, **kwargs)
