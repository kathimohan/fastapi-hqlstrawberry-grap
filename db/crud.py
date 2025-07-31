use sqlalchemy ; create a class which is having create, update, partial_update, delete, filter_delete methods ; it expects table name and dict ; the dict should have key as column name and value as data to be populated ; the value might forwighn key, text, jsondb, str, int, float ; update is for all cols update; if not provided any column then store None ; for partial_update if any column not provided then keep previus value as it is ; delete expects table name and primary key value and filter_delete expects tablename, primary_key and value to be deleted and it should filter all and delete all those

from sqlalchemy.orm import Session
from sqlalchemy import inspect, delete as sa_delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.inspection import inspect
from typing import Optional, List

class SQLAlchemyCRUD:
    def __init__(self, model):
        self.model = model

    def _get_columns(self):
        return {col.name for col in inspect(self.model).columns}

    @staticmethod
    def get_instance_data(instance, fields: Optional[List[str]] = None):
        # Get all column attributes from the instance
        column_attrs = inspect(instance).mapper.column_attrs
        # Get all data into a dict
        all_data = {c.key: getattr(instance, c.key) for c in column_attrs}
        # If specific fields are requested, filter and return them
        if fields:
            return {k: all_data[k] for k in fields if k in all_data}
        return all_data

    def create(self, session: Session, data: dict, fields: Optional[List[str]] = None):
        columns = self._get_columns()
        model_data = {k: data.get(k, None) for k in columns}
        instance = self.model(**model_data)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return self.get_instance_data(instance, fields)
    
    def update(self, session: Session, pk_value, data: dict, fields: Optional[List[str]] = None):
        instance = session.get(self.model, pk_value)
        if not instance:
            raise NoResultFound(f"No record found with primary key {pk_value}")
        
        columns = self._get_columns()
        for col in columns:
            setattr(instance, col, data.get(col, None))  # Full overwrite
        session.commit()
        session.refresh(instance)
        return self.get_instance_data(instance, fields)

    def partial_update(self, session: Session, pk_value, data: dict, fields: Optional[List[str]] = None):
        instance = session.get(self.model, pk_value)
        if not instance:
            raise NoResultFound(f"No record found with primary key {pk_value}")
        
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        session.commit()
        session.refresh(instance)
        return self.get_instance_data(instance, fields)

    def delete(self, session: Session, pk_value):
        instance = session.get(self.model, pk_value)
        if not instance:
            raise NoResultFound(f"No record found with primary key {pk_value}")
        session.delete(instance)
        session.commit()
        return True

    def filter_delete(self, session: Session, filter_col: str, filter_val):
        if not hasattr(self.model, filter_col):
            raise ValueError(f"{filter_col} is not a valid column")
        
        stmt = sa_delete(self.model).where(getattr(self.model, filter_col) == filter_val)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount  # Number of deleted rows


# usage :
    
crud = SQLAlchemyCRUD(Product)

# Create
product_data = {
    'name': 'Mouse',
    'price': 29.99,
    'description': 'Wireless mouse',
    'metadata': {'color': 'black'},
    'category_id': 1
}
product = crud.create(session, product_data)

# Update (full overwrite)
updated_data = {
    'name': 'Gaming Mouse',
    'price': 59.99,
    'description': 'RGB mouse',
    'metadata': {'color': 'black'},
    'category_id': 1
}
crud.update(session, pk_value=product.id, data=updated_data)

# Partial Update
crud.partial_update(session, pk_value=product.id, data={'price': 49.99})

# Delete by primary key
crud.delete(session, pk_value=product.id)

# Filter delete
crud.filter_delete(session, filter_col='category_id', filter_val=1)
