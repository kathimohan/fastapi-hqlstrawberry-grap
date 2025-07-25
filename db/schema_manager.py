import importlib
from sqlalchemy import create_engine, MetaData, Table, inspect, text, Column
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import ForeignKeyConstraint

# Shared Base to be used across all models
Base = declarative_base()

class DBSchemaManager:
    def __init__(self, engine):
        self.engine = engine
        self.connection = engine.connect()
        self.inspector = inspect(engine)
        self.metadata = Base.metadata

    def drop_all_tables(self):
        self.metadata.drop_all(self.engine)

    def drop_table(self, table_name: str):
        meta = MetaData()
        table = Table(table_name, meta, autoload_with=self.engine)
        table.drop(self.engine)

    def create_all_tables(self):
        self.metadata.create_all(self.engine)

    def create_table(self, model_class):
        model_class.__table__.create(self.engine)

    def add_column(self, table_name: str, column: Column):
        ddl = f"ALTER TABLE {table_name} ADD COLUMN {column.compile(dialect=self.engine.dialect)}"
        self.connection.execute(text(ddl))

    def drop_column(self, table_name: str, column_name: str):
        ddl = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        self.connection.execute(text(ddl))

    def rename_column(self, table_name: str, old_name: str, new_name: str):
        ddl = f'ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}'
        self.connection.execute(text(ddl))

    def update_table(self, model_class, rename_map: dict = None, apply_pk_change=False, apply_foreign_keys=False):
        """Update a specific table to match the model: rename, add, drop, change type, pk/fk."""
        table_name = model_class.__tablename__
        rename_map = rename_map or {}

        # Get current DB column info
        existing_cols = {col['name']: col for col in self.inspector.get_columns(table_name)}
        model_cols = {col.name: col for col in model_class.__table__.columns}

        # Rename columns
        for old_name, new_name in rename_map.items():
            if old_name in existing_cols and new_name not in existing_cols:
                print(f"[INFO] Renaming column: {old_name} → {new_name}")
                self.rename_column(table_name, old_name, new_name)
                existing_cols[new_name] = existing_cols.pop(old_name)

        # Add missing columns
        for name, col in model_cols.items():
            if name not in existing_cols:
                print(f"[INFO] Adding new column: {name}")
                self.add_column(table_name, col)

        # Drop extra columns
        model_col_names = set(model_cols.keys())
        existing_col_names = set(existing_cols.keys())
        for extra_col in existing_col_names - model_col_names:
            print(f"[INFO] Dropping extra column: {extra_col}")
            self.drop_column(table_name, extra_col)

        # Change type if needed
        for name, col in model_cols.items():
            if name in existing_cols:
                db_type = type(existing_cols[name]['type']).__name__
                model_type = type(col.type).__name__
                if db_type != model_type:
                    try:
                        ddl = f"ALTER TABLE {table_name} ALTER COLUMN {name} TYPE {col.type.compile(dialect=self.engine.dialect)} USING {name}::{col.type}"
                        print(f"[INFO] Changing type of {name}: {db_type} → {model_type}")
                        self.connection.execute(text(ddl))
                    except Exception as e:
                        print(f"[ERROR] Failed to change column type: {e}")

        # Handle primary key changes
        pk_db = set(self.inspector.get_pk_constraint(table_name)['constrained_columns'])
        pk_model = {col.name for col in model_class.__table__.columns if col.primary_key}

        if pk_db != pk_model:
            print(f"[WARNING] Primary key mismatch. DB: {pk_db}, Model: {pk_model}")
            if apply_pk_change:
                try:
                    self.connection.execute(text(f"ALTER TABLE {table_name} DROP CONSTRAINT {table_name}_pkey"))
                    pk_cols_str = ", ".join(pk_model)
                    self.connection.execute(text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_cols_str})"))
                    print(f"[INFO] Primary key changed to: {pk_model}")
                except Exception as e:
                    print(f"[ERROR] Failed to change primary key: {e}")
            else:
                print("[SKIPPED] Set apply_pk_change=True to apply primary key changes.")

        # Add missing foreign key constraints
        if apply_foreign_keys:
            existing_fks = {fk['constrained_columns'][0]: fk for fk in self.inspector.get_foreign_keys(table_name)}
            for constraint in model_class.__table__.constraints:
                if isinstance(constraint, ForeignKeyConstraint):
                    for fk_col in constraint.columns:
                        fk_name = fk_col.name
                        fk_target = list(constraint.elements)[0].target_fullname
                        if fk_name not in existing_fks:
                            fk_sql = f'ALTER TABLE {table_name} ADD CONSTRAINT fk_{fk_name} FOREIGN KEY ({fk_name}) REFERENCES {fk_target}'
                            try:
                                self.connection.execute(text(fk_sql))
                                print(f"[INFO] Foreign key added: {fk_name} → {fk_target}")
                            except Exception as e:
                                print(f"[ERROR] FK Add failed for {fk_name}: {e}")


# ----------------------
# Usage Example in main.py
# ----------------------
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from abc.db import dbmodel  # dbmodel.py contains all model classes using shared Base
    from abc.db.dbmodel import User, Group  # To refer specific model classes directly

    engine = create_engine("postgresql://user:password@localhost/dbname")

    # Initialize DBSchemaManager
    manager = DBSchemaManager(engine)

    # Register all models (should already be loaded from dbmodel)
    manager.create_all_tables()           # Create all tables
    manager.drop_all_tables()            # Drop all tables (optional)

    # Update specific model (with optional rename logic)
    rename_map = {"name": "full_name"}  # Optional: rename columns
    manager.update_table(User, rename_map=rename_map, apply_pk_change=True, apply_foreign_keys=True)

    # Create single table (if needed separately)
    manager.create_table(Group)
