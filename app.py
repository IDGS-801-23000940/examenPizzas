from flask import Flask, render_template
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db

# Instancia global del objeto Migrate para acceso desde CLI
migrate = Migrate()

def create_app(config_class=DevelopmentConfig):
    # Inicialización de la aplicación Flask
    app = Flask(__name__)
    
    # Cargar la configuración (usamos DevelopmentConfig por defecto)
    app.config.from_object(config_class)
    
    # Inicializar la extensión de SQLAlchemy con la app
    db.init_app(app)
    
    # Inicializar Flask-Migrate (Alembic) para migraciones de BD
    migrate.init_app(app, db)
    
    # Importar los Blueprints (se hace aquí para evitar importaciones circulares)
    from main.routes import main_bp
    from pedidos.routes import pedidos_bp
    from reportes.routes import reportes_bp
    
    # Registrar los Blueprints y definir sus prefijos de URL
    app.register_blueprint(main_bp)
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')

    # Manejador Global de Error 404
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
        
    # Crear las tablas en la base de datos si no existen al iniciar la app
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()