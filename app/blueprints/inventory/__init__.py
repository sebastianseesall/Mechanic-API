from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from . import routes  # Import routes after blueprint initialization 