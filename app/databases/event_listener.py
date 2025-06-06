from sqlalchemy import event
from app.databases.models.book import Book
from app.databases.models.audit import AuditLog
from app.databases.connection import SessionLocal

def after_insert_listener(mapper, connection, target):
    session = SessionLocal()
    log = AuditLog(
        action="CREATE",
        resource=target.__class__.__name__,
        resource_id=str(target.id),
        description=f"{target.__class__.__name__} created"
    )
    session.add(log)
    session.commit()


def event_listeners():
    event.listen(Book, 'after_insert', after_insert_listener)
