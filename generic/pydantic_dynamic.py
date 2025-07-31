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
