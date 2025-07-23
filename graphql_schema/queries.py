# graphql_schema/queries.py

import strawberry
from typing import List
from db.models import Sample
from graphql_schema.types import SampleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://username:password@localhost:5432/your_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@strawberry.type
class Query:
    @strawberry.field
    def list_samples(self) -> List[SampleType]:
        db = SessionLocal()
        try:
            samples = db.query(Sample).all()
            return samples
        finally:
            db.close()
