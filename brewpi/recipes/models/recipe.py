# -*- coding: utf-8 -*-
"""Recipe models."""

from pybeerxml.parser import Parser

from brewpi.database import Column, PkModel, db


class Recipe(PkModel):
    """A recipe."""

    __tablename__ = "recipe"
    name = Column(db.String(256), unique=False, nullable=True)
    xml = Column(db.String(128000), nullable=True)
    beerpy = Column(db.PickleType())

    def __init__(self, xml, **kwargs):
        """Create instance."""
        p = Parser()
        recipe = p.parse_from_string(xml)[0]
        name = recipe.name
        super().__init__(name=name, xml="", beerpy=recipe, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Recipe({self.name})>"
