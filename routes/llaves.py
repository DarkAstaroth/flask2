from flask import Blueprint, jsonify, request
from services.llaves import generar_llaves_service, obtener_llave_publica_service

llaves_bp = Blueprint("llaves", __name__)

@llaves_bp.route("/generar-llaves", methods=["POST"])
def generar_llaves_route():
    resultado = generar_llaves_service()
    return jsonify(resultado), 200

@llaves_bp.route("/llave-publica", methods=["GET"])
def obtener_llave_publica_route():
    resultado = obtener_llave_publica_service()
    return jsonify(resultado), 200