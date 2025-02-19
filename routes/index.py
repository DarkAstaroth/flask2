from flask import jsonify
from flask_restx import Namespace, Resource

api = Namespace("Index", description="Inicio de la aplicación")

@api.route("")
class IndexResource(Resource):
    def get(self):
        return {"estado": True}, 200
