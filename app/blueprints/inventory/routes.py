from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema

@inventory_bp.route("/", methods=['POST'])
def create_inventory():
    try:
        part_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(part_data)
    db.session.commit()
    return inventory_schema.jsonify(part_data), 201

@inventory_bp.route("/", methods=['GET'])
def get_inventory():
    query = select(Inventory)
    parts = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.route("/<int:part_id>", methods=['GET'])
def get_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found."}), 404
    return inventory_schema.jsonify(part), 200

@inventory_bp.route("/<int:part_id>", methods=['PUT', 'PATCH'])
def update_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found."}), 404
    for key, value in request.json.items():
        setattr(part, key, value)
    db.session.commit()
    return inventory_schema.jsonify(part), 200

@inventory_bp.route("/<int:part_id>", methods=['DELETE'])
def delete_part(part_id):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found."}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f'Part id: {part_id} successfully deleted.'}), 200