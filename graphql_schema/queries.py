# graphql_schema/queries.py

import strawberry
from typing import List
from graphql_schema.types import SampleType
from graphql_schema.resolvers import get_all_samples

@strawberry.type
class Query:
    list_samples: List[SampleType] = strawberry.field(resolver=get_all_samples)
