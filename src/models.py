from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'usuario'  # Corregido: nombre de la tabla en español
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)  # Corregido: unique=False no es necesario
    is_active = db.Column(db.Boolean(), nullable=False, default=True)  # Corregido: unique=False no es necesario

    def __repr__(self):
        return '<User %r>' % self.email  # Corregido: usar email en lugar de username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # No serializar la contraseña, es un riesgo de seguridad
        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    genero = db.Column(db.String(120), nullable=False)
    nacimiento = db.Column(db.String(120), nullable=False)
    favoritos = db.relationship('Favorito', backref='personaje', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "nacimiento": self.nacimiento
            
        }
class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    clima = db.Column(db.String(120), nullable=False)
    terreno = db.Column(db.String(120), nullable=False)
    favoritos = db.relationship('Favorito', backref='planeta', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno
            
        }

class Favorito(db.Model):
    __tablename__ = 'favorito'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'), nullable=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'), nullable=True)

    def to_dict(self):
        return {}

# Función para renderizar el esquema ER, si es necesario
def render_er_diagram():
    render_er(db.Model, 'er_diagram.png')

# Se puede invocar la función render_er_diagram para generar un diagrama ER
