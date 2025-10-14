from flask import Blueprint, jsonify, request

service_tickets_bp = Blueprint('service_tickets', __name__)

@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    """
    Create a new service ticket.
    """
    data = request.get_json()
    # Add logic to create a new service ticket using the data
    return jsonify({"message": "Service ticket created successfully"}), 201