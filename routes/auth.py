from flask import Blueprint, jsonify
import datetime
import jwt
from db_client import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/generar-token", methods=["POST"])
def generar_token():
    # Crear el token JWT
    token = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        "supersecretkey",  # Usar la clave secreta desde .env
        algorithm="HS256",
    )
    return jsonify({"token": token}), 200