from datetime import datetime
from sqlalchemy.orm import Session


def update_object(db: Session, info_to_update, object_in_db):
    """Updates an SQLAlchemy Object based on a Pydantic schema"""
    for key, value in info_to_update.__dict__.items():
        setattr(object_in_db, key, value)
        object_in_db.updated_date = datetime.utcnow()
    db.commit()
    db.refresh(object_in_db)
    return object_in_db
