#!/usr/bin/python3
"""State Module for HBNB project."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import models
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """State class."""

    if models.storage_type == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize a state."""
        super().__init__(*args, **kwargs)

        @property
        def cities(self):
            """Return a list of City instances with state_id equal to the current State.id."""
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
