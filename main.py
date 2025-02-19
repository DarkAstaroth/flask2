from flask import Flask,render_template
from database.db_client import db, init_db
from routes.auth import api as auth_api 
from routes.cifrado import api as cifrado_api
from routes.llaves import api as llaves_api
from routes.usuarios import api as usuarios_api
from routes.index import api as index_api
from flask_restx import Api 
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    api = Api(app, version="1.0", title="Documentación", description="Documentación con Swagger",doc="/docs")
    
    init_db(app)
    
    api.add_namespace(auth_api, path='/api/auth')
    api.add_namespace(cifrado_api, path='/api/datos')
    api.add_namespace(llaves_api, path='/api/llaves')
    api.add_namespace(usuarios_api, path='/api/usuarios')
    
    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)