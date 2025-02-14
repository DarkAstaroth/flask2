from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'postgresql://postgres:default@localhost:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Modelo para las llaves
class Llaves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    private_key = db.Column(db.Text, nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Llaves {self.id}>"

