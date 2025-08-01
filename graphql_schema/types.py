@strawberry.type
class SampleType:
    id: int
    parent_id: int
    json_data: dict
    score: float
    title: str
    description: str
    created_ts: datetime
    created_by: str
    modified_ts: datetime
    modified_by: Optional[str]
    pmpt: Optional[str]
    pmpt_id: Optional[int]


# graphql_schema/types.py
import strawberry
from typing import List, Optional, Union

@strawberry.type
class ProductType:
    id: int
    name: str
    category: str
    price: float

@strawberry.input
class SearchFilter:
    type: str  # "exact" or "contains"
    searchterm: str

@strawberry.input
class SearchCondition:
    name: Optional[List[SearchFilter]] = None
    category: Optional[List[SearchFilter]] = None

@strawberry.type
class SearchResult:
    results: List[ProductType]
    total_rows_count: int
    limit: Optional[int]
    offset: int
