"""
Flask Application Factory

Creates and configures the Flask application with Azure Key Vault integration.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config_by_name, kv_config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    config_class = config_by_name[config_name]
    app.config.from_object(config_class)

    # Validate production config
    if config_name == 'production':
        config_class.validate()

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # Register blueprints
    from app.routes.products import products_bp
    from app.routes.auth import auth_bp
    from app.routes.orders import orders_bp
    from app.routes.config import config_bp
    from app.routes.health import health_bp

    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(orders_bp, url_prefix='/api')
    app.register_blueprint(config_bp, url_prefix='/api/config')
    app.register_blueprint(health_bp, url_prefix='/api/health')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
