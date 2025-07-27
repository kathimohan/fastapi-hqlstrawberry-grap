from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
from your_app.models import MyModel  # Replace with your actual import

@event.listens_for(MyModel, "before_update")
def increment_version_on_status_change(mapper, connection, target):
    history = get_history(target, "status")
    if history.has_changes():
        target.version_id = (target.version_id or 0) + 1