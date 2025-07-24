# graphql_schema/resolvers.py

from db.models import Sample
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql://username:password@localhost:5432/your_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# CRUD Logic

def create_sample(
    parent_id: int,
    json_data: dict,
    score: float,
    title: str,
    description: str,
    pmpt: str,
    created_by: str
) -> Sample:
    db = SessionLocal()
    try:
        item = Sample(
            parent_id=parent_id,
            json_data=json_data,
            score=score,
            title=title,
            description=description,
            pmpt=pmpt,
            pmpt_id=1,
            created_ts=datetime.utcnow(),
            created_by=created_by,
            modified_ts=datetime.utcnow(),
            modified_by=created_by
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()


def update_sample(
    sample_id: int,
    title: str = None,
    description: str = None,
    pmpt: str = None,
    modified_by: str = None
) -> Sample:
    db = SessionLocal()
    try:
        item = db.query(Sample).filter(Sample.id == sample_id).first()
        if not item:
            raise Exception("Sample not found")
        
        if title:
            item.title = title
        if description:
            item.description = description
        if pmpt and item.pmpt != pmpt:
            item.pmpt = pmpt
            item.pmpt_id = (item.pmpt_id or 0) + 1

        item.modified_ts = datetime.utcnow()
        item.modified_by = modified_by or item.modified_by

        db.commit()
        db.refresh(item)
        return item
    finally:
        db.close()



def delete_sample(sample_id: int) -> str:
    db = SessionLocal()
    try:
        item = db.query(Sample).filter(Sample.id == sample_id).first()
        if not item:
            return "Sample not found"
        db.delete(item)
        db.commit()
        return "Sample deleted"
    finally:
        db.close()
