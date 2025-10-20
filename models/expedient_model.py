from database import db
import uuid

class Expediente(db.Model):
    __tablename__ = 'expediente'

    id = db.Column(db.String(128), primary_key=True, default=uuid.uuid4)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    dias_trabalho = db.Column(db.JSON, nullable=False)

    def to_map(self):
        return {
            'id': str(self.id),
            'horario_inicio': str(self.horario_inicio),
            'horario_fim': str(self.horario_fim),
            'dias_trabalho': self.dias_trabalho
        }
