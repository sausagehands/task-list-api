from flask import Blueprint, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task

from .route_utilities import *

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def send_task_ids():
    request_body = request.get_json()
    
    if "task_ids" in request_body:
        task_ids = request_body["task_ids"]
        
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            task.goal_id = goal_id 
        db.session.commit()
        return{
            "id": goal_id,
            "task_ids": task_ids
        }, 200


@bp.post("", strict_slashes = False)
def create_goal():
    return create_item(Goal)

@bp.post("/<goal_id>/tasks", strict_slashes = False)
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    if "task_ids" in request_body:
        task_ids = request_body["task_ids"]
        
        for task in goal.tasks:
            task.goal_id = None
        
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            task.goal_id = goal_id 
            
        db.session.commit()
        return{
            "id": goal.id,
            "task_ids": task_ids
        }, 200

    else:
        request_body["goal_id"] = goal.id
    
    # try:
    #     new_task = Task.from_dict(request_body)
        
    # except KeyError as error:
    #     response = {"message": f"Invalid request: missing {error.args[0]}"}
    #     abort(make_response(response, 400))
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        return make_response(new_task.to_dict(), 200) 

@bp.get("", strict_slashes = False)
def get_all_goals():
    return get_all_items(Goal)

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = [task.to_dict() for task in goal.tasks]
    return response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    return get_one_item(Goal, goal_id)

@bp.put("/<goal_id>", strict_slashes = False)
def update_entire_goal(goal_id):
    return update_entire_item(Goal, goal_id)

@bp.patch("/<goal_id>", strict_slashes = False)
def update_partial_goal(goal_id):
    return update_partial_item(Goal, goal_id)
    
@bp.patch("/<goal_id>/mark_complete", strict_slashes = False)
def mark_complete(goal_id):
    return mark_item_complete(Goal, goal_id)

@bp.patch("/<goal_id>/mark_incomplete", strict_slashes = False)
def mark_incomplete(goal_id):
    return mark_item_incomplete(Goal, goal_id)

@bp.delete("/<goal_id>", strict_slashes = False)
def delete_goal(goal_id):
    return delete_item(Goal, goal_id)