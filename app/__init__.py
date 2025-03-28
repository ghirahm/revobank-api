from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.account_routes import account_bp
    from app.routes.user_routes import user_bp
    from app.routes.transaction_routes import transaction_bp

    app.register_blueprint(account_bp, url_prefix="/accounts")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")

    return app
