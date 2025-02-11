from flask import Flask, jsonify,request, jsonify
import os
import jwt
import time
import requests

app = Flask(__name__)

@app.route('/logs', methods=['POST'])
def hola():
    body = request.get_json()  # Obtiene el cuerpo de la solicitud
    return jsonify(body), 200  # Retorna el mismo JSON recibido

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({"mensaje": "Hola"}), 200 

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
