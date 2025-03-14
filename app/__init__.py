from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///revobank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# Import routes di akhir buat hindari circular import
from app.routes import user_bp, account_bp, transaction_bp

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(account_bp, url_prefix='/accounts')
app.register_blueprint(transaction_bp, url_prefix='/transactions')