def generate_crud_routes(
    model: Type,
    router_tag: str,
    return_fields_on_create: Optional[List[str]] = None,
    partial_update_fields: Optional[List[str]] = None,
    route_prefix: Optional[str] = None  # <-- New parameter
) -> APIRouter:
    router = APIRouter(tags=[router_tag])
    crud = SQLAlchemyCRUD(model)
    
    # Fallback to model name if custom route prefix not provided
    prefix = route_prefix or model.__name__.lower()

    CreateSchema = generate_pydantic_model(model, name_suffix="Create")
    UpdateSchema = generate_pydantic_model(model, name_suffix="Update")
    PartialUpdateSchema = generate_pydantic_model(model, include_fields=partial_update_fields, name_suffix="PartialUpdate")
    OutputSchema = generate_pydantic_model(model, name_suffix="Out")

    @router.post(f"/{prefix}/create", response_model=OutputSchema)
    def create_item(data: CreateSchema, session: Session = Depends(get_session)):
        instance = crud.create(session, data.dict())
        return crud.get_instance_data(instance, return_fields_on_create)

    @router.put(f"/{prefix}/update/{{item_id}}", response_model=OutputSchema)
    def update_item(item_id: int, data: UpdateSchema, session: Session = Depends(get_session)):
        try:
            instance = crud.update(session, item_id, data.dict())
            return crud.get_instance_data(instance)
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.patch(f"/{prefix}/partial_update/{{item_id}}", response_model=OutputSchema)
    def partial_update_item(item_id: int, data: PartialUpdateSchema, session: Session = Depends(get_session)):
        try:
            instance = crud.partial_update(session, item_id, data.dict(exclude_unset=True))
            return crud.get_instance_data(instance)
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.delete(f"/{prefix}/delete", response_model=dict)
    def delete_item(item_id: int = Query(...), session: Session = Depends(get_session)):
        try:
            crud.delete(session, item_id)
            return {"status": "deleted"}
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.delete(f"/{prefix}/filter_delete", response_model=dict)
    def filter_delete(col: str = Query(...), val: Any = Query(...), session: Session = Depends(get_session)):
        try:
            count = crud.filter_delete(session, col, val)
            return {"deleted_count": count}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router
