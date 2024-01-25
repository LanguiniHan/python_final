from flask import Blueprint

product = Blueprint('products', __name__)

from routes.products import routes
