from database import db

class Adress(db.Model):
    __tablename__ = "adress"
    
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(255), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    
    complemento = db.Column(db.String(255), nullable=True)
    
    __table_args__ = (
        db.Index('idx_cep', 'cep'),
    )

    def __repr__(self):
        return f"<Endereco cidade={self.cidade} cep={self.cep}>"