from flask import Blueprint

category = Blueprint('category', __name__)

from routes.category import routes
