# graphql_schema/mutations.py

import strawberry
from graphql_schema.types import SampleType
from graphql_schema import resolvers


@strawberry.type
class SampleMutation:
    create_sample: SampleType = strawberry.field(resolver=resolvers.create_sample)
    update_sample: SampleType = strawberry.field(resolver=resolvers.update_sample)
    delete_sample: str = strawberry.field(resolver=resolvers.delete_sample)


@strawberry.type
class Mutation(SampleMutation):
    pass  # You can merge more mutation classes later
