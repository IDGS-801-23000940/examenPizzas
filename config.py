import os
from sqlalchemy import create_engine

class Config(object):
    # SECRET_KEY: Clave secreta para CSRF y sesiones. [cite: 82]
    SECRET_KEY = "ClaveSecreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    # DEBUG: True en desarrollo, False en producción. [cite: 82]
    DEBUG = True
    
    # SQLALCHEMY_DATABASE_URI: Conexión con driver PyMySQL [cite: 82]
    # Usamos tus credenciales (root:admin) pero apuntamos a la BD 'pizzas'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@127.0.0.1/pizzas'
    
    # SQLALCHEMY_TRACK_MODIFICATIONS: False (mejora rendimiento, elimina warnings). [cite: 82]
    SQLALCHEMY_TRACK_MODIFICATIONS = False