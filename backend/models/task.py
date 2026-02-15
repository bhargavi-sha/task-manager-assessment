from datetime import datetime
from enum import Enum
from . import db


class TaskStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.String(500))

    status = db.Column(
        db.Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.PENDING
    )

    due_date = db.Column(db.Date, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"
