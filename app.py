from flask import Flask,render_template
from database.db_client import db, init_db
from routes.auth import auth_bp
from routes.cifrado import cifrado_bp
from routes.llaves import llaves_bp
from routes.usuarios import usuarios_bp
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Inicializar la base de datos
    init_db(app)
    
    # Registrar rutas
    app.register_blueprint(auth_bp)
    app.register_blueprint(cifrado_bp)
    app.register_blueprint(llaves_bp)
    app.register_blueprint(usuarios_bp)
    
    return app

app = create_app()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)