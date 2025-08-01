1. ✅ graphql_schema/types.py (no changes if already like this)
python
Copy
Edit
import strawberry
from enum import Enum
from typing import Optional


@strawberry.enum
class SearchTypeEnum(Enum):
    EXACT = "exact"
    CONTAINS = "contains"


@strawberry.input
class SearchFilter:
    type: SearchTypeEnum
    searchterm: str


@strawberry.input
class SearchConditionsInput:
    key: str
    filters: list[SearchFilter]


@strawberry.input
class SearchQueryInput:
    conditions: Optional[list[SearchConditionsInput]] = None
    order_by: Optional[list[str]] = None
    limit: Optional[int] = None
    offset: Optional[int] = 0


@strawberry.type
class SampleType:
    id: int
    name: str
    price: float
    category: str


@strawberry.type
class SearchResultType:
    results: list[SampleType]
    total_rows_count: int
    limit: Optional[int]
    offset: Optional[int]
2. ✅ graphql_schema/resolvers.py
python
Copy
Edit
from sqlalchemy.orm import Session
from db import get_session
from models import Sample
from services.crud import SQLAlchemyCRUD
from graphql_schema.types import SampleType, SearchResultType, SearchQueryInput
from strawberry.types import Info


ALLOWED_RETURN_FIELDS = ["id", "name", "price", "category"]


def get_selected_fields_from_info(info: Info) -> list[str]:
    # Drill down into result selection: listSamplesWithSearch -> results -> fields
    for field in info.selected_fields:
        if field.name == "results":
            return [
                subfield.name
                for subfield in field.selections
                if subfield.name in ALLOWED_RETURN_FIELDS
            ]
    return ALLOWED_RETURN_FIELDS  # fallback


def get_samples_with_search(search: SearchQueryInput, info: Info) -> SearchResultType:
    session: Session = get_session()
    crud = SQLAlchemyCRUD(Sample)

    # Convert to search dict
    conditions = {}
    if search.conditions:
        for condition in search.conditions:
            conditions[condition.key] = [
                {"type": f.type.value, "searchterm": f.searchterm}
                for f in condition.filters
            ]

    # Only query fields requested by the user and allowed
    selected_fields = get_selected_fields_from_info(info)

    results_dict = crud.search(
        session=session,
        search_conditions=conditions or None,
        order_by=search.order_by,
        return_fields=selected_fields,
        limit=search.limit,
        offset=search.offset,
    )

    return SearchResultType(
        results=[SampleType(**r) for r in results_dict["results"]],
        total_rows_count=results_dict["total_rows_count"],
        limit=results_dict["limit"],
        offset=results_dict["offset"],
    )
3. ✅ graphql_schema/schema.py
python
Copy
Edit
import strawberry
from graphql_schema.types import SearchResultType, SearchQueryInput
from graphql_schema.resolvers import get_samples_with_search


@strawberry.type
class Query:
    list_samples_with_search: SearchResultType = strawberry.field(
        resolver=get_samples_with_search
    )


schema = strawberry.Schema(query=Query)
4. ✅ Your GraphQL Query
graphql
Copy
Edit
query {
  listSamplesWithSearch(
    search: {
      conditions: [
        {
          key: "name"
          filters: [{type: CONTAINS, searchterm: "mou"}]
        }
      ],
      orderBy: ["-price"],
      limit: 3
    }
  ) {
    results {
      id
      name
    }
    totalRowsCount
    limit
    offset
  }
}