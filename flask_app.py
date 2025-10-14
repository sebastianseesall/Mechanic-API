from app import create_app #gets function to create (flask)app
from app.models import db #imports db object
from app.blueprints.service_tickets import service_tickets_bp

from flask_marshmallow import Marshmallow
from flask import Blueprint, jsonify, send_from_directory


ma = Marshmallow() #sets up marshmallow (serialization/deserialization library)

app = create_app('ProductionConfig') #creates app using config from config.py

from sqlalchemy import text


with app.app_context(): 
    db.create_all() #creates all tables in db (if they don't already exist)
    # with db.engine.connect() as conn:
    #     conn.execute(text('ALTER TABLE service_ticket_inventory ADD COLUMN quantity INT NOT NULL DEFAULT 1;'))



@app.route('/swagger.yaml')
def swagger_spec():
    return send_from_directory('.', 'swagger.yaml') 

def some_function():
    ticket = {}  # Assuming ticket is defined somewhere
    return jsonify(service_ticket_schema.dump(ticket)), 201

