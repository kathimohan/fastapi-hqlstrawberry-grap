from fastapi import FastAPI
from your_app.models import Customer
from your_app.routes.generator import generate_crud_routes

create 5 fast apis -- create , update, partial_update, delete and filter_delete  . Actually it should be one call from backend side, there backend coder pass only table name , api router tag, and what to return for create instead of whole instance, the coder pass list which should return ; if not passed any return all elements of db class ; partial_upadte - coder pass which elements to allow for show in swagger page, delete expects id in swagger page, filter_delete expects column_name and value

app = FastAPI()

# Default: all APIs, model name as prefix
app.include_router(generate_crud_routes(
    model=Customer,
    router_tag="Customer",
))

# Custom route prefix and only selected APIs
app.include_router(generate_crud_routes(
    model=MyModel,
    router_tag="MyModelOps",
    route_prefix="mymodel-api",
    return_fields_on_create=["id", "status", "version_id"],
    partial_update_fields=["status"],
    expose_apis=["create", "partial_update"]  # Only these will show up
    
))
