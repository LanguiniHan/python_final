from flask import Blueprint

customer = Blueprint('customers', __name__)

from routes.customers import routes
