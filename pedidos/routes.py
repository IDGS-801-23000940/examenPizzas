from flask import render_template, request, redirect, url_for, flash, session
from . import pedidos_bp
from forms import PedidoForm
from models import db, Cliente, Pedido, DetallePedido, Pizza
import uuid
from datetime import date

PRECIOS_TAMANO = {'Chica': 40.00, 'Mediana': 80.00, 'Grande': 120.00}
PRECIO_INGREDIENTE = 10.00

@pedidos_bp.route('/nuevo')
def nuevo_pedido():
    """Render the order form page."""
    form = PedidoForm()
    
    # Load saved client data from session if available
    if 'cliente_temp' in session:
        c = session['cliente_temp']
        form.nombre.data = c.get('nombre')
        form.direccion.data = c.get('direccion')
        form.telefono.data = c.get('telefono')
        if c.get('fecha'):
            try:
                form.fecha.data = date.fromisoformat(c.get('fecha'))
            except:
                pass
                
    return render_template('index.html', form=form)

@pedidos_bp.route('/agregar', methods=['POST'])
def agregar_pizza():
    form = PedidoForm(request.form)
    
    # Save client data in session for persistence
    session['cliente_temp'] = {
        'nombre': form.nombre.data,
        'direccion': form.direccion.data,
        'telefono': form.telefono.data,
        'fecha': form.fecha.data.isoformat() if form.fecha.data else date.today().isoformat()
    }
    
    if form.tamano.data:
        tamano = form.tamano.data
        ingredientes_seleccionados = form.ingredientes.data or []
        cantidad = form.num_pizzas.data or 1
        
        costo_base = PRECIOS_TAMANO[tamano]
        costo_ingredientes = len(ingredientes_seleccionados) * PRECIO_INGREDIENTE
        subtotal = (costo_base + costo_ingredientes) * cantidad
        
        linea_pedido = {
            'id_temp': str(uuid.uuid4()),
            'tamano': tamano,
            'ingredientes': ', '.join(ingredientes_seleccionados) if ingredientes_seleccionados else 'Sin ingredientes extra',
            'cantidad': cantidad,
            'subtotal': float(subtotal)
        }
        
        if 'carrito' not in session:
            session['carrito'] = []
            
        session['carrito'].append(linea_pedido)
        session.modified = True
        flash(f'Pizza {tamano} agregada correctamente.', 'success')
    else:
        flash('Debes seleccionar un tamaño para la pizza.', 'error')
        
    return redirect(url_for('pedidos.nuevo_pedido'))

@pedidos_bp.route('/quitar/<id_temp>', methods=['POST'])
def quitar_pizza(id_temp):
    form = PedidoForm(request.form)
    session['cliente_temp'] = {
        'nombre': form.nombre.data,
        'direccion': form.direccion.data,
        'telefono': form.telefono.data,
        'fecha': form.fecha.data.isoformat() if form.fecha.data else date.today().isoformat()
    }
    
    if 'carrito' in session:
        session['carrito'] = [item for item in session['carrito'] if item['id_temp'] != id_temp]
        session.modified = True
        flash('Pizza eliminada del pedido.', 'info')
    return redirect(url_for('pedidos.nuevo_pedido'))

@pedidos_bp.route('/terminar', methods=['POST'])
def terminar_pedido():
    form = PedidoForm(request.form)
    carrito = session.get('carrito', [])
    
    if not carrito:
        flash('El carrito está vacío. Agrega al menos una pizza.', 'warning')
        return redirect(url_for('pedidos.nuevo_pedido'))
    
    nombre = form.nombre.data or (session.get('cliente_temp', {}).get('nombre'))
    direccion = form.direccion.data or (session.get('cliente_temp', {}).get('direccion'))
    telefono = form.telefono.data or (session.get('cliente_temp', {}).get('telefono'))
    fecha_val = form.fecha.data
    
    if not fecha_val and session.get('cliente_temp', {}).get('fecha'):
        try:
            fecha_val = date.fromisoformat(session['cliente_temp']['fecha'])
        except:
            fecha_val = date.today()

    if not all([nombre, direccion, telefono, fecha_val]):
        if not nombre: form.nombre.errors.append("El nombre es obligatorio para terminar.")
        if not direccion: form.direccion.errors.append("La dirección es obligatoria.")
        if not telefono: form.telefono.errors.append("El teléfono es obligatorio.")
        if not fecha_val: form.fecha.errors.append("La fecha es obligatoria.")
        flash("Por favor completa los datos del cliente para finalizar.", "error")
        return render_template('index.html', form=form)

    try:
        cliente = Cliente.query.filter_by(nombre=nombre, telefono=telefono).first()
        if not cliente:
            cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono)
            db.session.add(cliente)
            db.session.flush()
            
        total_pedido = sum(item['subtotal'] for item in carrito)
        nuevo_pedido = Pedido(id_cliente=cliente.id_cliente, fecha=fecha_val, total=total_pedido)
        db.session.add(nuevo_pedido)
        db.session.flush()
        
        for item in carrito:
            pizza_ref = Pizza.query.filter_by(tamano=item['tamano'], ingredientes=item['ingredientes']).first()
            if not pizza_ref:
                pizza_ref = Pizza(tamano=item['tamano'], ingredientes=item['ingredientes'], precio=PRECIOS_TAMANO[item['tamano']])
                db.session.add(pizza_ref)
                db.session.flush()
                
            detalle = DetallePedido(id_pedido=nuevo_pedido.id_pedido, id_pizza=pizza_ref.id_pizza, cantidad=item['cantidad'], subtotal=item['subtotal'])
            db.session.add(detalle)
            
        db.session.commit()
        
        session.pop('carrito', None)
        session.pop('cliente_temp', None)
        flash(f'¡Pedido de {nombre} registrado con éxito! Total: ${total_pedido:.2f}', 'success')
        return redirect(url_for('pedidos.nuevo_pedido'))
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR DB: {e}")
        flash('Error al guardar en la base de datos. Intente nuevamente.', 'error')
        return render_template('index.html', form=form)

@pedidos_bp.route('/detalle/<int:id_pedido>')
def detalle_pedido(id_pedido):
    """Show order details."""
    pedido = Pedido.query.get_or_404(id_pedido)
    return render_template('pedidos/detalle.html', pedido=pedido)

