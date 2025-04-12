from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.routes.user_routes import user_bp
    from app.routes.account_routes import account_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.budget_routes import budgets_bp
    from app.routes.transaction_category_routes import transaction_category_bp
    from app.routes.bill_routes import bill_bp
    from app.auth.routes import auth_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(account_bp, url_prefix="/accounts")
    app.register_blueprint(transaction_bp, url_prefix="/transactions")
    app.register_blueprint(budgets_bp, url_prefix="/budgets")
    app.register_blueprint(transaction_category_bp, url_prefix="/transactions")
    app.register_blueprint(bill_bp, url_prefix="/bills")
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
