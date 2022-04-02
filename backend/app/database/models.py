from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Table,
)
from sqlalchemy.orm import relationship, declarative_mixin
from sqlalchemy.sql import func
from app.database.connector import Base


@declarative_mixin
class TimestampMixin:
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, nullable=True)


class User(TimestampMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    super_admin = Column(Boolean, default=False)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class PlaceList(TimestampMixin, Base):
    __tablename__ = "placelists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship(
        "User",
        primaryjoin="PlaceList.owner_id == User.id",
        backref="placelists",
    )
    places = relationship("Place", secondary="place_placelist")


class Place(TimestampMixin, Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    google_place_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    owner = relationship(
        "User",
        primaryjoin="Place.owner_id == User.id",
        backref="places",
    )
    placelists = relationship(
        "PlaceList", secondary="place_placelist", overlaps="places"
    )


place_placelist = Table(
    "place_placelist",
    Base.metadata,
    Column("place_id", Integer, ForeignKey("places.id")),
    Column("placelist_id", Integer, ForeignKey("placelists.id")),
)
