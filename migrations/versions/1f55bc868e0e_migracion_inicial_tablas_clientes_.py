"""migracion inicial: tablas clientes, pedidos, pizzas, detalle_pedido

Revision ID: 1f55bc868e0e
Revises: 
Create Date: 2026-03-13 23:03:38.832377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f55bc868e0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Esquema inicial de la base de datos 'pizzas' ###
    
    op.create_table('clientes',
        sa.Column('id_cliente', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('direccion', sa.String(length=200), nullable=False),
        sa.Column('telefono', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id_cliente')
    )

    op.create_table('pizzas',
        sa.Column('id_pizza', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tamano', sa.String(length=20), nullable=False),
        sa.Column('ingredientes', sa.String(length=200), nullable=False),
        sa.Column('precio', sa.Numeric(precision=8, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('id_pizza')
    )

    op.create_table('pedidos',
        sa.Column('id_pedido', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_cliente', sa.Integer(), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(['id_cliente'], ['clientes.id_cliente']),
        sa.PrimaryKeyConstraint('id_pedido')
    )

    op.create_table('detalle_pedido',
        sa.Column('id_detalle', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('id_pedido', sa.Integer(), nullable=False),
        sa.Column('id_pizza', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('subtotal', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(['id_pedido'], ['pedidos.id_pedido']),
        sa.ForeignKeyConstraint(['id_pizza'], ['pizzas.id_pizza']),
        sa.PrimaryKeyConstraint('id_detalle')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### Revertir migración: eliminar todas las tablas ###
    op.drop_table('detalle_pedido')
    op.drop_table('pedidos')
    op.drop_table('pizzas')
    op.drop_table('clientes')
    # ### end Alembic commands ###
