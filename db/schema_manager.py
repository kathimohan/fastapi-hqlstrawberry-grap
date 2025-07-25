from sqlalchemy import create_engine, MetaData, Table, Column, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import ProgrammingError

Base = declarative_base()

class DBSchemaManager:
    def __init__(self, engine):
        self.engine = engine
        self.metadata = Base.metadata
        self.connection = engine.connect()

    def drop_all_tables(self):
        self.metadata.drop_all(self.engine)
        print("All tables dropped.")

    def drop_table(self, table_name: str):
        meta = MetaData()
        table = Table(table_name, meta, autoload_with=self.engine)
        table.drop(self.engine)
        print(f"Table '{table_name}' dropped.")

    def create_all_tables(self):
        self.metadata.create_all(self.engine)
        print("All tables created.")

    def create_table(self, model_class):
        model_class.__table__.create(self.engine)
        print(f"Table '{model_class.__tablename__}' created.")

    def add_column(self, table_name: str, column: Column):
        ddl = f"ALTER TABLE {table_name} ADD COLUMN {column.compile(dialect=self.engine.dialect)}"
        try:
            self.connection.execute(text(ddl))
            print(f"Added column '{column.name}' to table '{table_name}'.")
        except ProgrammingError as e:
            print(f"Failed to add column: {e}")

    def drop_column(self, table_name: str, column_name: str):
        ddl = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
        try:
            self.connection.execute(text(ddl))
            print(f"Dropped column '{column_name}' from table '{table_name}'.")
        except ProgrammingError as e:
            print(f"Failed to drop column: {e}")

    def rename_column(self, table_name: str, old_name: str, new_name: str, col_type):
        ddl = f'ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}'
        try:
            self.connection.execute(text(ddl))
            print(f"Renamed column '{old_name}' to '{new_name}' in table '{table_name}'.")
        except ProgrammingError as e:
            print(f"Failed to rename column: {e}")


## usage
            
from sqlalchemy import create_engine, Column, Integer, String

# Define your model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Initialize
engine = create_engine("postgresql://username:password@localhost/dbname")
manager = DBSchemaManager(engine)

# Drop/create
manager.drop_table("users")
manager.create_table(User)

# Add a column
new_col = Column("email", String)
manager.add_column("users", new_col)

# Drop a column
manager.drop_column("users", "email")

# Rename a column (ensure DB supports it)
manager.rename_column("users", "name", "full_name", String)

# Drop all tables
manager.drop_all_tables()