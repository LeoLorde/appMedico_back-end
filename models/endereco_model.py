from database import db

class Address(db.Model):
    __tablename__ = "address"
    
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(255), nullable=False)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    
    complemento = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Endereco cidade={self.cidade} cep={self.cep}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "cidade": self.cidade,
            "estado": self.estado,
            "cep": self.cep,
            "rua": self.rua,
            "numero": self.numero,
            "complemento": self.complemento,
        }