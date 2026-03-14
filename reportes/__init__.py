from flask import Blueprint

reportes_bp = Blueprint('reportes', __name__)

from . import routes