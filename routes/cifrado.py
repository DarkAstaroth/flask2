from flask import Blueprint, jsonify, request
from services.cifrado import cifrar_mensaje, descifrar_mensaje

cifrado_bp = Blueprint("cifrado", __name__)

@cifrado_bp.route("/cifrado-hibrido", methods=["POST"])
def cifrado_hibrido_route():
    data = request.get_json()
    mensaje = data["mensaje"]
    public_key_base64 = data["public_key"]
    resultado = cifrar_mensaje(mensaje, public_key_base64)
    return jsonify(resultado), 200

@cifrado_bp.route("/descifrar", methods=["POST"])
def descifrar_route():
    data = request.get_json()
    datos_cifrados = data["datos"]
    clave_simetrica_cifrada = data["clave_simetrica"]
    iv = data["iv"]
    resultado = descifrar_mensaje(datos_cifrados, clave_simetrica_cifrada, iv)
    return jsonify(resultado), 200