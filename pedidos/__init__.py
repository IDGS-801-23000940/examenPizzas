from flask import Blueprint

pedidos_bp = Blueprint('pedidos', __name__)

from . import routes