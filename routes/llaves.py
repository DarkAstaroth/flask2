from flask import Blueprint, jsonify
from flask_restx import  Namespace, Resource, fields
from services.llaves import generar_llaves_service, obtener_llave_publica_service

api = Namespace("Llaves", description="Operaciones para gestionar llaves")


llave_response_model = api.model("LlaveResponse", {
    "public_key": fields.String(description="Llave pública en base64", example="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."),
    "fecha_creacion": fields.String(description="Fecha de creación de la llave", example="2025-02-19T13:00:00")
})

error_response_model = api.model("ErrorResponse", {
    "error": fields.String(description="Mensaje de error", example="No se ha encontrado ninguna llave pública en la base de datos.")
})

generar_llaves_response_model = api.model("GenerarLlavesResponse", {
    "id": fields.Integer(description="ID de la llave generada", example=1),
    "private_key": fields.String(description="Llave privada en base64", example="MIIBOwIBAAJBALJ6r0i2rQhXbHq7IrlLs..."),
    "public_key": fields.String(description="Llave pública en base64", example="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A..."),
    "fecha_creacion": fields.String(description="Fecha de creación de la llave", example="2025-02-19T13:00:00")
})

@api.route("/generar-llaves", methods=["POST"])
class GenerarLlavesResource(Resource):
    @api.marshal_with(generar_llaves_response_model, code=200)
    def post(self):
        """Genera un par de llaves pública y privada RSA y las guarda en la base de datos"""
        resultado = generar_llaves_service()
        return resultado, 200

@api.route("/llave-publica")
class ObtenerLlavePublicaResource(Resource):
    @api.marshal_with(llave_response_model, code=200)
    @api.response(404, 'Llave pública no encontrada', error_response_model)
    def get(self):
        """Obtiene la llave pública desde la base de datos"""
        resultado = obtener_llave_publica_service()

        if "error" in resultado:
            return resultado, 404

        return resultado, 200 
