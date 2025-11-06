from flask import Blueprint, abort, make_response, request, jsonify
from app.models.goal import Goal
from app.models.task import Task

from .route_utilities import *

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def associate_tasks_with_goal(goal, task_ids):
    '''clear old associations-- this seems kind of dumb, what if i'm trying to append more tasks?
    can you append to an endpoint like that? would it be a patch? an update?'''
    for task in goal.tasks:
        task.goal_id = None
    
    #add new tasks
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
    
    db.session.commit()
    
    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200

def create_new_task_for_goal(goal, task_data):
    task_data["goal_id"] = goal.id
    
    '''if i remove request_body from create_item helper function, i can technically reuse it here?
    but then i have to refactor everything again... ugggh-- i'd also have to remove its return
    statement since that one has 201 & this one 200'''
    new_task = Task.from_dict(task_data)
    db.session.add(new_task)
    db.session.commit
    
    return new_task.to_dict(), 200

@bp.post("", strict_slashes = False)
def create_goal():
    return create_item(Goal)

@bp.post("/<goal_id>/tasks", strict_slashes = False)
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    if "task_ids" in request_body:
        task_ids = request_body["task_ids"]
        return associate_tasks_with_goal(goal, task_ids)

    else:
        return create_new_task_for_goal


@bp.get("", strict_slashes = False)
def get_all_goals():
    return get_all_items(Goal)

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return{
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    return get_one_item(Goal, goal_id)

@bp.put("/<goal_id>", strict_slashes = False)
def update_entire_goal(goal_id):
    updated_goal = update_entire_item(Goal, goal_id, goal_update=True)
    return jsonify(updated_goal.to_dict()), 200


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