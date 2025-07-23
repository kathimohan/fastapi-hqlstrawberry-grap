# graphql_schema/mutations.py

import strawberry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Sample
from datetime import datetime

DATABASE_URL = "postgresql://username:password@localhost:5432/your_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_sample(
        self,
        parent_id: int,
        json_data: dict,
        score: float,
        title: str,
        description: str,
        pmpt: str
    ) -> str:
        db = SessionLocal()
        try:
            sample = Sample(
                parent_id=parent_id,
                json_data=json_data,
                score=score,
                title=title,
                description=description,
                created_at=datetime.utcnow(),
                pmpt=pmpt,
                pmpt_id=1
            )
            db.add(sample)
            db.commit()
            return "Sample created"
        finally:
            db.close()

    @strawberry.mutation
    def update_sample(
        self,
        sample_id: int,
        title: str = None,
        description: str = None,
        pmpt: str = None
    ) -> str:
        db = SessionLocal()
        try:
            sample = db.query(Sample).filter(Sample.id == sample_id).first()
            if not sample:
                return "Sample not found"

            if title:
                sample.title = title
            if description:
                sample.description = description

            if pmpt and sample.pmpt != pmpt:
                sample.pmpt = pmpt
                sample.pmpt_id = (sample.pmpt_id or 0) + 1

            db.commit()
            return "Sample updated"
        finally:
            db.close()
