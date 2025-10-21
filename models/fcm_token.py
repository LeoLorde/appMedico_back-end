from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from database import db

class FcmToken(db.Model):
    __tablename__ = 'fcm_tokens'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String(20), nullable=False)  # 'client' ou 'doctor'
    fcm_token = Column(String, nullable=False, unique=True)
    device_info = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint("user_type IN ('client', 'doctor')", name='check_user_type'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'fcm_token': self.fcm_token,
            'device_info': self.device_info,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }