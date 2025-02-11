from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/hola', methods=['GET'])
def hola():
    return jsonify({"mensaje": "Hola"}), 200 

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
