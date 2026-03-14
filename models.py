from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    
    # Relación uno a muchos con Pedido. cascade="all, delete" cumple la regla referencial.
    pedidos = db.relationship('Pedido', backref='cliente', cascade="all, delete", lazy=True)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    
    # Relación uno a muchos con DetallePedido. cascade="all, delete" cumple la regla referencial.
    detalles = db.relationship('DetallePedido', backref='pedido', cascade="all, delete", lazy=True)

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id_pizza = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tamano = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Numeric(8, 2), nullable=False)
    
    # No hay cascada de eliminación hacia detalles para mantener el historial (como dictan las reglas).
    detalles = db.relationship('DetallePedido', backref='pizza', lazy=True)

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    
    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_pizza = db.Column(db.Integer, db.ForeignKey('pizzas.id_pizza'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False) # La restricción CHECK > 0 se suele manejar en BD o validación de formulario
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)