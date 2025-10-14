from app import create_app #gets function to create (flask)app
from app.models import db #imports db object

from flask_marshmallow import Marshmallow
from flask import Blueprint, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

ma = Marshmallow() #sets up marshmallow (serialization/deserialization library)

app = create_app('ProductionConfig') #creates app using config from config.py

SWAGGER_URL = '/swagger'
API_URL = '/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from sqlalchemy import text

with app.app_context(): 
    db.create_all() #creates all tables in db (if they don't already exist)
    # with db.engine.connect() as conn:
    #     conn.execute(text('ALTER TABLE service_ticket_inventory ADD COLUMN quantity INT NOT NULL DEFAULT 1;'))

if __name__ == "__main__":
    app.run()

@app.route('/swagger.yaml')
def swagger_spec():
    return send_from_directory('.', 'swagger.yaml')

def some_function():
    ticket = {}  # Assuming ticket is defined somewhere
    return jsonify(service_ticket_schema.dump(ticket)), 201

@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    """
    ---
    tags:
      - service_tickets
    summary: Create a new service ticket
    description: Creates a new service ticket for a customer and vehicle.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/ServiceTicketPayload'
    responses:
      201:
        description: Service ticket created
        schema:
          $ref: '#/definitions/ServiceTicketResponse'
      400:
        description: Validation error
    definitions:
      ServiceTicketPayload:
        type: object
        properties:
          customer_id:
            type: integer
          VIN:
            type: string
          service_description:
            type: string
          service_date:
            type: string
            format: date
        required:
          - customer_id
          - VIN
          - service_description
          - service_date

      ServiceTicketResponse:
        type: object
        properties:
          id:
            type: integer
          customer_id:
            type: integer
          VIN:
            type: string
          service_description:
            type: string
          service_date:
            type: string
            format: date
    """
    # ...existing code...

