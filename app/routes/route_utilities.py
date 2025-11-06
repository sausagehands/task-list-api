from flask import abort, make_response, request, Response
from ..db import db
from datetime import datetime
import os
import requests

def validate_model(cls, id):
    try:
        id = int(id)
    except: 
        response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response , 400))
    
    query = db.select(cls).where(cls.id == id)
    item = db.session.scalar(query)
    
    if not item: #for database, use <if not> because scalar(query) returns None
        response = {"message": f"{cls.__name__} {id} not found"}
        abort(make_response(response, 404))
    
    return item

def send_slack_notification(item_title):
    slack_token = os.environ.get("SLACK_TOKEN")
    if slack_token:
        try:
            requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {slack_token}"},
            json={
                "channel": "slack-api-testing",
                "text": f"Someone just completed {item_title}"
                }
            )
        except Exception as e:
            print(f"Slack notification failed: {e}")
            
def create_item(cls):
    request_body = request.get_json()
    
    try:
        new_item = cls.from_dict(request_body)
        
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_item)
    db.session.commit()
    
    return new_item.to_dict(), 201

def get_all_items(cls):
    query = db.select(cls)
    #can i move this to a helper function? its getting long as heckums
    title_param = request.args.get('title')
    if title_param:
        query = query.where(cls.title.ilike(f"{title_param}%"))
    
    
    sort_param = request.args.get('sort', 'asc')
    
    
    if sort_param == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.title.asc())
        
    items = db.session.scalars(query)
    
    items_response = []
    for item in items:
        items_response.append(item.to_dict())
    return items_response

def get_one_item(cls, id):
    item = validate_model(cls, id)
    
    return item.to_dict()

def update_entire_item(cls, id):
    item = validate_model(cls, id)
    request_body = request.get_json()
    
    item.title = request_body["title"]
    item.description = request_body["description"]
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")


def update_partial_item(cls, id):
    item = validate_model(cls, id)
    request_body = request.get_json()
    
    if 'title' in request_body:
        item.title = request_body['title']
    
    if 'description' in request_body:
        item.description = request_body['description']
    
    if 'is_complete' in request_body:
        if request_body['is_complete']:
            item.completed_at = datetime.now()
        else:
            item.completed_at = None
        
    db.session.commit()
        
    return Response(status=204, mimetype="application/json")

def mark_item_complete(cls, id):
    item = validate_model(cls, id)
    
    item.completed_at = datetime.now()
    
    db.session.commit()
    
    send_slack_notification(item.title)
    
    return Response(status=204, mimetype="application/json")

def mark_item_incomplete(cls, id):
    item = validate_model(cls, id)
    
    item.completed_at = None
    
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")

def delete_item(cls, id):
    item = validate_model(cls, id)
    
    db.session.delete(item)
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")