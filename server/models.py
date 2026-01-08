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
    Serialisation - conversion of a python obj to something simpler, universal like json
    recursion - Heroes have many powers, Power has many heroes
    When Heroes is serialised it contains powers
    Each power tries to include its hero
    That power includes its hero causing an endless loop
    """
    serialize_rules = ("-hero_powers.hero",)


class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship: A power has many HeroPowers

    hero_powers = db.relationship(
        "HeroPower", back_populates="power", cascade="all, delete-orphan"
    )

    serialize_rules = ("-hero_powers.power", )  # Preventing infinite recursion loop

    # Validation 1 : description must have  at least 20 chars
    # Error raised if condition is nto met
    # This is important for data integrity

    @validates("description")  # Runs automatically when you try to set the description
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(
        db.Integer, db.ForeignKey("heroes.id")
    )  # Foreign Keys to reference id columns in heroes tables
    power_id = db.Column(
        db.Integer, db.ForeignKey("powers.id")
    )  # Foreign Keys to reference id columns in powers table

    # Relationships: HeroPower belongs to Hero and Power

    hero = db.relationship(
        "Hero", back_populates="hero_powers"
    )  # Back populates creates a 2 way connection
    power = db.relationship("Power", back_populates="hero_powers")

    # Prevent infinite recursion again

    serialize_rules = (
        "-hero.hero_powers",
        "-power.hero_powers",
    )

    # "-" sign means when serializing include the hero but don't include the hero_powers inside the hero

    # validation 2: Strength must be Strong weak or avg

    @validates("strength")
    def validate_strength(self, key, strength):
        validate_strengths = ["Strong", "Weak", "Average"]
        if strength not in validate_strengths:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return strength
