from fastapi import FastAPI
from your_app.models import Customer
from your_app.routes.generator import generate_crud_routes

create 5 fast apis -- create , update, partial_update, delete and filter_delete  . Actually it should be one call from backend side, there backend coder pass only table name , api router tag, and what to return for create instead of whole instance, the coder pass list which should return ; if not passed any return all elements of db class ; partial_upadte - coder pass which elements to allow for show in swagger page, delete expects id in swagger page, filter_delete expects column_name and value

app = FastAPI()

# Custom path prefix: /client/...
app.include_router(generate_crud_routes(
    model=Customer,
    router_tag="CustomerOps",
    route_prefix="client",  # 👈 Optional custom prefix
    return_fields_on_create=["id", "email"],
    partial_update_fields=["email"]
))

# Default path: /customer/...
app.include_router(generate_crud_routes(
    model=Customer,
    router_tag="CustomerOps",
    return_fields_on_create=["id", "email"],
    partial_update_fields=["email"]
))
