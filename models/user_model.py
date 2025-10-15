from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from abc import abstractmethod, ABC
from datetime import datetime

class User(ABC, db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(128))
    
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @abstractmethod
    def __repr__(self):
        return f"<User | id: ${self.id} | username: ${self.username}"