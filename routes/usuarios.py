from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields
from services.usuarios import listar_usuarios_service, crear_usuario_service, buscar_usuario_service, eliminar_usuario_service

api = Namespace("Usuarios", description="Operaciones para gestionar usuarios fake")

# Modelos para la documentación Swagger

usuario_model = api.model("Usuario", {
    "id": fields.Integer(description="ID del usuario", example=1),
    "nombre": fields.String(description="Nombre del usuario", example="Juan"),
    "paterno": fields.String(description="Apellido paterno del usuario", example="Pérez"),
    "materno": fields.String(description="Apellido materno del usuario", example="González"),
    "fecha_nacimiento": fields.String(description="Fecha de nacimiento del usuario", example="1990-05-01"),
    "carnet": fields.String(description="Carnet del usuario", example="12345678A"),
    "sexo": fields.String(description="Sexo del usuario", example="Masculino")
})

error_response_model = api.model("ErrorResponse", {
    "error": fields.String(description="Mensaje de error", example="Usuario con ID 100 no encontrado")
})

# Ruta para listar usuarios
@api.route("/listar", methods=["POST"])
class ListarUsuariosResource(Resource):
    @api.marshal_with(usuario_model, as_list=True, code=200)
    def post(self):
        """Listar todos los usuarios"""
        usuarios = listar_usuarios_service()
        return usuarios, 200

# Ruta para crear un nuevo usuario
@api.route("/crear", methods=["POST"])
class CrearUsuarioResource(Resource):
    @api.expect(usuario_model)  # Indica que la entrada debe ser conforme al modelo de usuario
    @api.marshal_with(usuario_model, code=201)
    def post(self):
        """Crear un nuevo usuario"""
        data = request.get_json()
        resultado = crear_usuario_service(data)
        return resultado, 201

# Ruta para buscar un usuario
@api.route("/buscar", methods=["POST"])
class BuscarUsuarioResource(Resource):
    @api.expect(fields.Integer(description="ID del usuario a buscar", example=1))
    @api.marshal_with(usuario_model, code=200)
    @api.response(404, "Usuario no encontrado", error_response_model)
    def post(self):
        """Buscar un usuario por ID"""
        data = request.get_json()
        resultado = buscar_usuario_service(data["id"])
        
        if "error" in resultado:
            return resultado, 404
        
        return resultado, 200

# Ruta para eliminar un usuario
@api.route("/eliminar", methods=["POST"])
class EliminarUsuarioResource(Resource):
    @api.expect(fields.Integer(description="ID del usuario a eliminar", example=1))
    @api.marshal_with(error_response_model, code=200)
    def post(self):
        """Eliminar un usuario por ID"""
        data = request.get_json()
        resultado = eliminar_usuario_service(data["id"])
        return resultado, 200
