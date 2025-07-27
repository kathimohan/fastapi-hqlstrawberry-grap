from pydantic import BaseModel, create_model
from typing import Optional, Type
from sqlalchemy.inspection import inspect

def generate_pydantic_model(model_class, include_fields=None, name_suffix="Schema") -> Type[BaseModel]:
    mapper = inspect(model_class)
    fields = {}
    for column in mapper.columns:
        if include_fields and column.name not in include_fields:
            continue
        python_type = column.type.python_type
        fields[column.name] = (Optional[python_type], None)
    model_name = f"{model_class.__name__}{name_suffix}"
    return create_model(model_name, **fields)
