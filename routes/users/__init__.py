from flask import Blueprint

user = Blueprint('users', __name__)

from routes.users import routes
