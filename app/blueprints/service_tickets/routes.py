from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, db, Mechanic  # Make sure Mechanic is imported
from . import service_tickets_bp

@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(ticket_data)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket_data), 201

@service_tickets_bp.route("/", methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)

@service_tickets_bp.route("/<int:ticket_id>", methods=['GET'])
def get_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if ticket:
        return service_ticket_schema.jsonify(ticket), 200
    return jsonify({"error": "Service ticket not found."}), 404

@service_tickets_bp.route("/<int:ticket_id>", methods=['PUT', 'PATCH'])
def update_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    service_ticket_schema.session = db.session
    try:
        ticket_data = service_ticket_schema.load(request.json, instance=ticket, partial=True)
    except ValidationError as e:
        return jsonify(getattr(e, "messages", str(e))), 400
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route("/<int:ticket_id>", methods=['DELETE'])
def delete_service_ticket(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": f'Service ticket id: {ticket_id}, successfully deleted.'}), 200

#ADVANCED ENDPOINT 

@service_tickets_bp.route("/<int:ticket_id>/edit", methods=["PUT"])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404

    data = request.get_json() or {}
    add_ids = data.get("add_ids", [])
    remove_ids = data.get("remove_ids", [])

    # Remove mechanics
    if remove_ids:
        for mech_id in remove_ids:
            mechanic = db.session.get(Mechanic, mech_id)
            if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)

    # Add mechanics
    if add_ids:
        for mech_id in add_ids:
            mechanic = db.session.get(Mechanic, mech_id)
            if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)

    db.session.commit()
    return jsonify({
        "message": "Mechanics updated successfully.",
        "ticket": {
            "id": ticket.id,
            "mechanics": [m.id for m in ticket.mechanics]
        }
    }), 200
