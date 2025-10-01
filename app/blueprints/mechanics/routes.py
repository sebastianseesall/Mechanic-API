from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp

@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(mechanic_data)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic_data), 201

@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

@mechanics_bp.route("/<int:mechanic_id>", methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic not found."}), 404

@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT', 'PATCH'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    mechanic_schema.session = db.session
    try:
        mechanic_data = mechanic_schema.load(request.json, instance=mechanic, partial=True)
    except ValidationError as e:
        return jsonify(getattr(e, "messages", str(e))), 400
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200

# ADVANCED ENDPOINT
@mechanics_bp.route("/ranked", methods=["GET"])
def get_mechanics_ranked():

    mechanics = db.session.query(Mechanic).all()


    sorted_mechanics = sorted(
        mechanics,
        key=lambda m: len(m.service_tickets),  
        reverse=True
    )

    response = [
        {"id": m.id, "name": m.first_name, "ticket_count": len(m.service_tickets)}
        for m in sorted_mechanics
    ]

    return jsonify(response), 200

@mechanics_bp.route("/search", methods=['GET'])
def search_mechanics():
    name = request.args.get("name", "")
    email = request.args.get("email", "")

    query = select(Mechanic)

    if name:
        query = query.where(Mechanic.first_name.ilike(f"%{name}%"))  # Adjust field name if needed
    if email:
        query = query.where(Mechanic.email.ilike(f"%{email}%"))

    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200
