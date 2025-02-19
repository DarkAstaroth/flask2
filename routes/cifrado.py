from flask import request
from flask_restx import Namespace, Resource, fields
from services.cifrado import cifrar_mensaje, descifrar_mensaje

api = Namespace("Datos", description="Operaciones de cifrado")

cifrado_model = api.model("CifradoRequest", {
    "mensaje": fields.String(required=True, description="Mensaje a cifrar"),
    "public_key": fields.String(required=True, description="Clave pública en base64"),
})

descifrado_model = api.model("DescifradoRequest", {
    "datos": fields.String(required=True, description="Datos cifrados"),
    "clave_simetrica": fields.String(required=True, description="Clave simétrica cifrada"),
    "iv": fields.String(required=True, description="Vector de inicialización"),
})

respuesta_model = api.model("CifradoResponse", {
    "datos": fields.String(description="Mensaje cifrado en base64"),
    "clave_simetrica": fields.String(description="Clave simétrica cifrada"),
    "iv": fields.String(description="Vector de inicialización"),
})

@api.route("/cifrar")
class CifradoHibridoResource(Resource):
    @api.expect(cifrado_model)
    @api.marshal_with(respuesta_model)
    def post(self):
        """Cifra un mensaje con cifrado híbrido"""
        data = request.get_json()
        mensaje = data["mensaje"]
        public_key_base64 = data["public_key"]
        resultado = cifrar_mensaje(mensaje, public_key_base64)
        return resultado, 200


@api.route("/descifrar")
class DescifrarResource(Resource):
    @api.expect(descifrado_model)
    def post(self):
        """Descifra un mensaje cifrado"""
        data = request.get_json()
        datos_cifrados = data["datos"]
        clave_simetrica_cifrada = data["clave_simetrica"]
        iv = data["iv"]
        resultado = descifrar_mensaje(datos_cifrados, clave_simetrica_cifrada, iv)
        return resultado, 200
