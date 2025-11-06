from flask import Blueprint
from app.models.goal import Goal

from .route_utilities import *

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("", strict_slashes = False)
def create_goal():
    return create_item(Goal)

@bp.get("", strict_slashes = False)
def get_all_goals():
    return get_all_items(Goal)

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