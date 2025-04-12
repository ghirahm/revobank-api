from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(db.Model):
    # __tablename__ = 'user'

    # Define the primary key column for the User model
    id = db.Column(db.Integer, primary_key=True)

    # Unique and required username for the user
    username = db.Column(db.String(255), unique=True, nullable=False)

    # Unique and required email address for the user
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Securely hashed password stored in the database
    password_hash = db.Column(db.String(255), nullable=False)

    # Timestamp for when the user was created (default: current UTC time)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Timestamp for when the user was last updated (auto-updated on changes)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # One-to-many relationship: one user can have many accounts
    # 'Account' is the related model, and 'user' is the reverse relationship on Account model
    accounts = db.relationship('Account', back_populates='user', cascade='all, delete-orphan')

    # Hash and store the given plaintext password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='scrypt')

    # Verify a given plaintext password against the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
