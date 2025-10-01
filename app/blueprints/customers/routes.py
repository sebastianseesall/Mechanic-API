from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp
from app.extensions import limiter, cache
from app.utils.util import encode_token


#login route
@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials.email  # Access as attribute
        password = credentials.password
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.check_password(password):
        token = encode_token(customer.id)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid email or password."}), 401


# CREATE CUSTOMER
@customers_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")  #A client can only attempt to make 3 users per hour
@cache.cached(timeout=60)  #Cache the response for 60 seconds
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
        password=customer_data.password
    )

    # Check for existing customer
    query = select(Customer).where(Customer.email == customer_data.email)
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already exists."}), 400

    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


# READ ALL CUSTOMERS with pagination
@customers_bp.route("/", methods=['GET'])
def get_customers():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    pagination = db.session.query(Customer).paginate(page=page, per_page=per_page, error_out=False)
    customers = pagination.items

    return jsonify({
        "customers": customers_schema.dump(customers),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    }), 200


#GET SPECIFIC MEMBER
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_member(customer_id):
    customer = db.session.get(Customer, customer_id)  # use lowercase 'customer'

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404

# UPDATE SPECIFIC CUSTOMER
@customers_bp.route("/<int:customer_id>", methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    customer_schema.session = db.session  # <-- Add this line

    try:
        customer_data = customer_schema.load(request.json, instance=customer, partial=True)
    except ValidationError as e:
        return jsonify(getattr(e, "messages", str(e))), 400

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# PATCH SPECIFIC CUSTOMER
@customers_bp.route("/<int:id>", methods=['PATCH'])
def patch_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Use request.json to get the update fields
    for key, value in request.json.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


# DELETE SPECIFIC CUSTOMER
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id}, successfully deleted.'}), 200
