from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields
import datetime
import jwt
from database.db_client import db

api = Namespace("Autenticación", description="Operaciones de autenticación")

token_response_model = api.model("TokenResponse", {
    "token": fields.String(description="JWT generado", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
})

auth_bp = Blueprint("auth", __name__)

@api.route("/generar-token")
class GenerarTokenResource(Resource):
    @api.marshal_with(token_response_model)
    def post(self):
        """Genera un token JWT para autenticación"""
        # Crear el token JWT
        token = jwt.encode(
            {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            "supersecretkey",  # Usar la clave secreta desde .env (mejor usar `os.getenv("SECRET_KEY")`)
            algorithm="HS256",
        )
        return {"token": token}, 200

# Registra el Blueprint con el namespace de Swagger
auth_bp.add_url_rule("/generar-token", view_func=GenerarTokenResource.as_view("generar_token"))
