from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import datetime

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mi_aplicacion.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Crear tablas en la base de datos
    with app.app_context():
        db.create_all()

# Modelo para las llaves
class Llaves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    private_key = db.Column(db.Text, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Llaves {self.id}>"