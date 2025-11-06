from flask import Blueprint
from app.models.task import Task
from .route_utilities import *


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("", strict_slashes = False)
def create_task():
    return create_item(Task)

@bp.get("", strict_slashes = False)
def get_all_tasks():
    return get_all_items(Task)

@bp.get("/<task_id>")
def get_one_task(task_id):
    return get_one_item(Task, task_id)

@bp.put("/<task_id>", strict_slashes = False)
def update_entire_task(task_id):
    update_entire_item(Task, task_id)
    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>", strict_slashes = False)
def update_partial_task(task_id):
    return update_partial_item(Task, task_id)
    
@bp.patch("/<task_id>/mark_complete", strict_slashes = False)
def mark_complete(task_id):
    return mark_item_complete(Task, task_id)

@bp.patch("/<task_id>/mark_incomplete", strict_slashes = False)
def mark_incomplete(task_id):
    return mark_item_incomplete(Task, task_id)

@bp.delete("/<task_id>", strict_slashes = False)
def delete_task(task_id):
    return delete_item(Task, task_id)


    
    
    