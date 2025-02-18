from flask import Blueprint, jsonify, request
from services.usuarios import listar_usuarios_service, crear_usuario_service, buscar_usuario_service, eliminar_usuario_service

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios/listar", methods=["POST"])
def listar_usuarios_route():
    usuarios = listar_usuarios_service()
    return jsonify(usuarios), 200

@usuarios_bp.route("/usuarios/crear", methods=["POST"])
def crear_usuario_route():
    data = request.get_json()
    resultado = crear_usuario_service(data)
    return jsonify(resultado), 201

@usuarios_bp.route("/usuarios/buscar", methods=["POST"])
def buscar_usuario_route():
    data = request.get_json()
    resultado = buscar_usuario_service(data["id"])
    return jsonify(resultado), 200

@usuarios_bp.route("/usuarios/eliminar", methods=["POST"])
def eliminar_usuario_route():
    data = request.get_json()
    resultado = eliminar_usuario_service(data["id"])
    return jsonify(resultado), 200