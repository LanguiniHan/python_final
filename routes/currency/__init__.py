from flask import Blueprint

currency = Blueprint('currency', __name__)

from routes.currency import routes
