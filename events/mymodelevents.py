from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
from your_app.models import MyModel  # Replace with your actual import

# Triggered before update
@event.listens_for(MyModel, "before_update")
def increment_version_on_any_change(mapper, connection, target):
    state = inspect(target)

    # Check if any column has changed (excluding version_id itself)
    changed = any(
        attr.history.has_changes()
        for attr in state.attrs.values()
        if attr.key != "version_id"
    )

    if changed:
        target.version_id = (target.version_id or 0) + 1

# Triggered before insert
@event.listens_for(MyModel, "before_insert")
def initialize_version_id(mapper, connection, target):
    if target.version_id is None:
        target.version_id = 1  # or 0, your choice


import listeners.my_model_events 