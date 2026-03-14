from flask_wtf import FlaskForm
from wtforms import StringField, DateField, RadioField, SelectMultipleField, IntegerField, SelectField, widgets
from wtforms.validators import DataRequired, Length, Regexp, NumberRange, Optional
from datetime import date

# Custom widget para renderizar múltiples checkboxes de forma limpia
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PedidoForm(FlaskForm):
    # RN-C01 a RN-C04: Datos del Cliente
    nombre = StringField('Nombre', validators=[DataRequired(message="El nombre es obligatorio"), Length(min=3, max=100)])
    direccion = StringField('Dirección', validators=[DataRequired(message="La dirección es obligatoria"), Length(min=5, max=200)])
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio"), 
        Regexp(r'^\d[\d\s-]{6,19}$', message="Use solo dígitos, espacios o guiones (7-20 caracteres)")
    ])
    fecha = DateField('Fecha del Pedido', validators=[DataRequired(message="La fecha es obligatoria")], default=date.today)
    
    # RN-P01 a RN-P04: Datos de la Pizza - Marcados como Optional para no bloquear el "Terminar Pedido"
    tamano = RadioField('Tamaño', choices=[
        ('Chica', 'Chica ($40)'), 
        ('Mediana', 'Mediana ($80)'), 
        ('Grande', 'Grande ($120)')
    ], validators=[Optional()])
    
    ingredientes = MultiCheckboxField('Ingredientes Adicionales ($10 c/u)', choices=[
        ('Jamon', 'Jamón'), 
        ('Piña', 'Piña'), 
        ('Champiñones', 'Champiñones')
    ], validators=[Optional()])
    
    num_pizzas = IntegerField('Cantidad', validators=[
        Optional(),
        NumberRange(min=1, message="La cantidad debe ser al menos 1")
    ], default=1)

class ConsultaVentasForm(FlaskForm):
    # Formulario para las consultas de reportes [cite: 63, 64, 65]
    tipo_consulta = SelectField('Tipo de Consulta', choices=[('dia', 'Por Día'), ('mes', 'Por Mes')])
    valor = StringField('Día o Mes (ej. Lunes, Enero)', validators=[DataRequired()])