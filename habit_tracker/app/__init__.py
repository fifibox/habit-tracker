"""
app package – creates and configures the Flask application.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from app.config import Config 
from flask_mail import Mail
from app.forms import ResetPasswordForm

# ------------------------------------------------------------------
# Extensions (created once, initialised later inside create_app())
# ------------------------------------------------------------------
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

def create_app(config: dict = None) -> Flask:
    """Application factory"""
    app = Flask(__name__, static_folder="static")
    app.config.from_object(Config)

    if config:
        app.config.from_mapping(config)

    # ----------------------------------------------------------------
    # Initialise extensions WITH the app instance
    # ----------------------------------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  
    login_manager.login_message = "Please log in to access this page."
    csrf.init_app(app)
    mail.init_app(app)

    # ----------------------------------------------------------------
    # Inject reset token form into all templates
    # ----------------------------------------------------------------
    @app.context_processor
    def inject_reset_token_form():
        return dict(reset_token_form=ResetPasswordForm())

    # ----------------------------------------------------------------
    # Register blueprints
    # ----------------------------------------------------------------
    from app.auth import auth_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # ----------------------------------------------------------------
    # Create tables on first run (optional)
    # ----------------------------------------------------------------
    with app.app_context():
        db.create_all()

    return app