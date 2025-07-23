# create_models.py

from db.models import Base
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://username:password@localhost:5432/your_db"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
