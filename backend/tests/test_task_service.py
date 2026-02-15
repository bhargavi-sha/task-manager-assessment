import pytest
from datetime import date

from app import create_app
from models import db
from models.task import Task, TaskStatus
from services.task_service import (
    create_task,
    update_task_status,
    InvalidStateTransition
)


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True
    })

    with app.app_context():
        db.drop_all()   # ensure clean
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_create_task(app):
    with app.app_context():
        task = create_task(
            title="Test Task",
            description="Test Description",
            due_date=date.today()
        )

        assert task.id is not None
        assert task.status == TaskStatus.PENDING


def test_valid_status_transition(app):
    with app.app_context():
        task = create_task(
            title="Test Task",
            description="Test Description",
            due_date=date.today()
        )

        updated_task = update_task_status(task.id, TaskStatus.IN_PROGRESS)

        assert updated_task.status == TaskStatus.IN_PROGRESS


def test_invalid_status_transition(app):
    with app.app_context():
        task = create_task(
            title="Test Task",
            description="Test Description",
            due_date=date.today()
        )

        update_task_status(task.id, TaskStatus.IN_PROGRESS)

        with pytest.raises(InvalidStateTransition):
            update_task_status(task.id, TaskStatus.PENDING)
