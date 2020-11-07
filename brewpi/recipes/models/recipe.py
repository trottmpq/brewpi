# -*- coding: utf-8 -*-
"""Recipe models."""

from pybeerxml.parser import Parser

from brewpi.database import Column, PkModel, db


class Recipe(PkModel):
    """A recipe."""

    __tablename__ = "recipe"
    name = Column(db.String(80), unique=False, nullable=True)
    xml = Column(db.String(128), nullable=False)
    beerpy = Column(db.PickleType())

    def __init__(self, xml, **kwargs):
        """Create instance."""
        p = Parser()
        recipe = p.parse(xml)[0]
        name = recipe.name
        super().__init__(name=name, xml=xml, beerpy=recipe, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Recipe({self.name})>"
