from database import db
from datetime import datetime
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    data = db.Column(db.JSON, nullable=True)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'title': self.title,
            'body': self.body,
            'type': self.type,
            'data': self.data,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }