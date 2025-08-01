from typing import Optional, Type, List
from pydantic import BaseModel, create_model
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta

def generate_pydantic_model(
    model_class: Type[DeclarativeMeta],
    include_fields: List[str] = None,
    name_suffix: str = "Schema",
    default: bool = False,
) -> Type[BaseModel]:
    mapper = inspect(model_class)
    fields = {}

    for column in mapper.columns:
        if include_fields and column.name not in include_fields:
            continue

        python_type = column.type.python_type

        # Get default value if requested
        if default:
            # SQLAlchemy column.default can be a DefaultClause or plain value
            col_default = column.default.arg if column.default is not None else None
            fields[column.name] = (Optional[python_type], col_default)
        else:
            fields[column.name] = (Optional[python_type], None)

    model_name = f"{model_class.__name__}{name_suffix}"
    return create_model(model_name, **fields)




import strawberry
from typing import Optional, Any, List
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Text, String, Integer, Float, Boolean, DateTime


SQLA_TYPE_MAPPING = {
    JSONB: dict,
    Text: str,
    String: str,
    Integer: int,
    Float: float,
    Boolean: bool,
    DateTime: str,
    # Add more mappings if needed
}


def get_python_type(column_type):
    try:
        return column_type.python_type
    except NotImplementedError:
        return SQLA_TYPE_MAPPING.get(type(column_type), Any)


def generate_strawberry_type_from_model(
    model_class: DeclarativeMeta,
    include_fields: Optional[List[str]] = None,
    type_name: Optional[str] = None
):
    mapper = inspect(model_class)
    annotations = {}

    for column in mapper.columns:
        if include_fields and column.name not in include_fields:
            continue

        python_type = get_python_type(column.type)
        if column.nullable:
            annotations[column.name] = Optional[python_type]
        else:
            annotations[column.name] = python_type

    type_name = type_name or f"{model_class.__name__}Type"
    return strawberry.type(type(type_name, (), annotations))
