from flask import render_template
from . import main_bp
from models import db, Pedido, Cliente
from datetime import date

@main_bp.route('/')
def index():
    """Welcome page with today's stats and recent orders."""
    hoy = date.today()
    
    # Today's stats
    pedidos_hoy = Pedido.query.filter(Pedido.fecha == hoy).all()
    num_pedidos_hoy = len(pedidos_hoy)
    ventas_hoy = sum(float(p.total) for p in pedidos_hoy)
    clientes_total = Cliente.query.count()
    
    return render_template('welcome.html',
        pedidos_hoy=num_pedidos_hoy,
        ventas_hoy=ventas_hoy,
        clientes_total=clientes_total,
        pedidos_recientes=pedidos_hoy
    )