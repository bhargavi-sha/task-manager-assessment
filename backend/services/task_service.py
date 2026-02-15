from datetime import date
from models.task import Task, TaskStatus
from models import db


class InvalidStateTransition(Exception):
    pass


class InvalidDueDate(Exception):
    pass


ALLOWED_TRANSITIONS = {
    TaskStatus.PENDING: [TaskStatus.IN_PROGRESS],
    TaskStatus.IN_PROGRESS: [TaskStatus.COMPLETED],
    TaskStatus.COMPLETED: []
}


def create_task(title: str, description: str, due_date):
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    if due_date < date.today():
        raise InvalidDueDate("Due date cannot be in the past")

    task = Task(
        title=title.strip(),
        description=description,
        due_date=due_date
    )

    db.session.add(task)
    db.session.commit()

    return task


def update_task_status(task_id: int, new_status: TaskStatus):
    task = Task.query.get(task_id)

    if not task:
        raise ValueError("Task not found")

    if new_status not in ALLOWED_TRANSITIONS[task.status]:
        raise InvalidStateTransition(
            f"Cannot move from {task.status.value} to {new_status.value}"
        )

    task.status = new_status
    db.session.commit()

    return task
