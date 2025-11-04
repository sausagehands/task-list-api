from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    
    return task.to_dict()


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except: 
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response , 400))
    
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task: #for database, use <if not> because scalar(query) returns None
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))
    
    return task

@tasks_bp.get("", strict_slashes = False)
def get_all_tasks():
    query = db.select(Task)
    
    title_param = request.args.get('title')
    

@tasks_bp.post("", strict_slashes = False)
def create_task():
    request_body = request.get_json()
    
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()
    
    return new_task.to_dict(), 201

@tasks_bp.put("", strict_slashes = False)
def update_task