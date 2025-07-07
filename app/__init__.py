from flask import Flask
from flask_bootstrap import Bootstrap5
from .main import main_bp
from .models import db, migrate
from .auth import auth_bp
from .admin import admin_bp
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap = Bootstrap5(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debe identificarse para acceder a esta página'
    login_manager.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)

    from .models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    return app


