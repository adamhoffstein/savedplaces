from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Numeric,
)
from sqlalchemy.orm import relationship, backref, declarative_mixin
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


class Place(TimestampMixin, Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    google_place_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)


# class SavedPlace(TimestampMixin, Base):
#     __tablename__ = "savedplaces"
#     __mapper_args__ = {"confirm_deleted_rows": False}
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     place_id = Column(Integer, ForeignKey("places.id"))

#     user = relationship(
#         User, backref=backref("saved", cascade="all, delete-orphan")
#     )

#     place = relationship(
#         Place, backref=backref("saved", cascade="all, delete-orphan")
#     )
