from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import text
from . import reportes_bp
from forms import ConsultaVentasForm
from models import db
from datetime import date

# Day/month mappings
DIAS_SEMANA = {
    'domingo': 1, 'lunes': 2, 'martes': 3, 'miercoles': 4, 'miércoles': 4,
    'jueves': 5, 'viernes': 6, 'sabado': 7, 'sábado': 7
}

MESES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}

@reportes_bp.route('/', methods=['GET', 'POST'])
def reportes():
    """Unified reports view. Shows today's orders by default, or search by day/month."""
    form = ConsultaVentasForm()
    resultados = []
    total_acumulado = 0
    busqueda = ""

    if request.method == 'POST' and form.validate_on_submit():
        tipo = form.tipo_consulta.data
        valor_input = form.valor.data.strip().lower()
        
        if tipo == 'dia':
            busqueda = f"Día: {valor_input.title()}"
            if valor_input not in DIAS_SEMANA:
                flash(f"El valor '{form.valor.data}' no corresponde a un día válido. Usa: lunes, martes, …, domingo.", 'error')
            else:
                num_dia = DIAS_SEMANA[valor_input]
                sql = text("""
                    SELECT p.id_pedido, c.nombre, p.fecha, p.total 
                    FROM pedidos p 
                    JOIN clientes c ON p.id_cliente = c.id_cliente 
                    WHERE DAYOFWEEK(p.fecha) = :num_dia 
                    ORDER BY p.fecha DESC
                """)
                result = db.session.execute(sql, {'num_dia': num_dia}).fetchall()
                if result:
                    resultados = result
                    total_acumulado = sum(float(row.total) for row in result)
                else:
                    flash(f"No se encontraron ventas para el día {valor_input}.", 'info')
        
        elif tipo == 'mes':
            busqueda = f"Mes: {valor_input.title()}"
            if valor_input not in MESES:
                flash(f"El valor '{form.valor.data}' no corresponde a un mes válido. Usa: enero, febrero, …, diciembre.", 'error')
            else:
                num_mes = MESES[valor_input]
                sql = text("""
                    SELECT p.id_pedido, c.nombre, p.fecha, p.total 
                    FROM pedidos p 
                    JOIN clientes c ON p.id_cliente = c.id_cliente 
                    WHERE MONTH(p.fecha) = :num_mes 
                    ORDER BY p.fecha ASC
                """)
                result = db.session.execute(sql, {'num_mes': num_mes}).fetchall()
                if result:
                    resultados = result
                    total_acumulado = sum(float(row.total) for row in result)
                else:
                    flash(f"No se encontraron ventas para el mes de {valor_input}.", 'info')
    else:
        # Default: show today's orders
        hoy = date.today()
        sql = text("""
            SELECT p.id_pedido, c.nombre, p.fecha, p.total 
            FROM pedidos p 
            JOIN clientes c ON p.id_cliente = c.id_cliente 
            WHERE p.fecha = :fecha_hoy
            ORDER BY p.id_pedido DESC
        """)
        result = db.session.execute(sql, {'fecha_hoy': hoy}).fetchall()
        if result:
            resultados = result
            total_acumulado = sum(float(row.total) for row in result)

    return render_template('reportes/reportes.html', 
        form=form, 
        resultados=resultados, 
        total=total_acumulado, 
        busqueda=busqueda
    )

# Keep old routes as redirects for backwards compatibility
@reportes_bp.route('/dia', methods=['GET'])
def ventas_dia():
    return redirect(url_for('reportes.reportes'))

@reportes_bp.route('/mes', methods=['GET'])
def ventas_mes():
    return redirect(url_for('reportes.reportes'))