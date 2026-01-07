from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates


db = SQLAlchemy()

"""
Hero - has many Powers (through HeroPower)
Power - has many Heroes (through HeroPower)
HeroPower - the join table that connects them
"""


class Hero(db.Model, SerializerMixin):
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # The relationship to HeroPower

    hero_powers = db.relationship(
        "HeroPower", back_populates="hero", cascade="all, delete-orphan"
    )

    # Cascade ensures that if hero is deleted the heroes powers are deleted too

    # Serialization rule to prevent infinite recursion

    """
    serialisation - conversion of a python obj to something simpler, universal like json
    recursion - Heroes have many powers, Power has many heroes
    When Heroes is serialised it contains powers
    Each power tries to include its hero
    That power includes its hero causing an endless loop
    """
    serialize_rules = ("-hero_powers.hero",)
