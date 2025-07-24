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
