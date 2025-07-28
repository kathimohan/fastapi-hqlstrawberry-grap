from fastapi import FastAPI
from your_app.models import Customer
from your_app.routes.generator import generate_crud_routes

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
