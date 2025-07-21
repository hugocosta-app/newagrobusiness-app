from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Create upload folders if they don't exist
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Ensure subfolder for visit photos exists
    visit_photo_folder = os.path.join(upload_folder, 'visits')
    if not os.path.exists(visit_photo_folder):
        os.makedirs(visit_photo_folder)

    # Register Blueprints
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.products import bp as products_bp
    app.register_blueprint(products_bp)

    from app.routes.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from app.routes.expenses import bp as expenses_bp
    app.register_blueprint(expenses_bp)

    from app.routes.visits import bp as visits_bp
    app.register_blueprint(visits_bp)

    from app.routes.agenda import bp as agenda_bp
    app.register_blueprint(agenda_bp)

    # Add a context processor to make 'now' available in templates for the year in footer
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}
    
    # Add context processor for allowed photo extensions (using config.py)
    @app.context_processor
    def inject_allowed_photo_extensions():
        return dict(ALLOWED_PHOTO_EXTENSIONS=app.config['ALLOWED_EXTENSIONS'])

    # Create database tables if they don't exist
    with app.app_context():
        # Import models here to ensure they are known to SQLAlchemy before create_all
        from app.models import user, product, order, expense, visit, agenda 
        db.create_all()

    # Add CLI commands
    from app import commands
    app.cli.add_command(commands.cli)

    return app

