from flask import Blueprint, request, jsonify
from datetime import datetime
from models.task import TaskStatus
from services.task_service import (
    create_task,
    update_task_status,
    InvalidStateTransition,
    InvalidDueDate
)

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("/", methods=["POST"], strict_slashes=False)



def create():
    try:
        data = request.get_json()

        title = data.get("title")
        description = data.get("description", "")
        due_date_str = data.get("due_date")

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        task = create_task(title, description, due_date)

        return jsonify({
            "id": task.id,
            "message": "Task created successfully"
        }), 201

    except InvalidDueDate as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


@task_bp.route("/<int:task_id>/status", methods=["PUT"])
def update_status(task_id):
    try:
        data = request.get_json()
        status_str = data.get("status")

        new_status = TaskStatus(status_str)

        task = update_task_status(task_id, new_status)

        return jsonify({
            "id": task.id,
            "new_status": task.status.value
        })

    except InvalidStateTransition as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Unexpected error"}), 500
    
@task_bp.route("/test", methods=["GET"])
def test_route():
    return {"message": "Blueprint working"}
from models.task import Task

@task_bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status.value,
            "due_date": t.due_date.isoformat()
        }
        for t in tasks
    ])


