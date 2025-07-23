# graphql_schema/types.py

import strawberry
from typing import Optional
from datetime import datetime

@strawberry.type
class SampleType:
    id: int
    parent_id: int
    json_data: dict
    score: float
    title: str
    description: str
    created_at: datetime
    pmpt: Optional[str]
    pmpt_id: Optional[int]
