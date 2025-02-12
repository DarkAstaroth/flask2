from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Fake DB (lista de usuarios) con 10 usuarios predefinidos
usuarios = [
    {"id": 1, "nombre": "Juan", "paterno": "Pérez", "materno": "Gómez", "fecha_nacimiento": "1990-01-01", "carnet": "123456", "sexo": "M"},
    {"id": 2, "nombre": "María", "paterno": "López", "materno": "García", "fecha_nacimiento": "1992-05-15", "carnet": "654321", "sexo": "F"},
    {"id": 3, "nombre": "Carlos", "paterno": "Martínez", "materno": "Rodríguez", "fecha_nacimiento": "1985-11-30", "carnet": "987654", "sexo": "M"},
    {"id": 4, "nombre": "Ana", "paterno": "González", "materno": "Fernández", "fecha_nacimiento": "1998-07-22", "carnet": "456789", "sexo": "F"},
    {"id": 5, "nombre": "Luis", "paterno": "Hernández", "materno": "Díaz", "fecha_nacimiento": "1993-03-10", "carnet": "321654", "sexo": "M"},
    {"id": 6, "nombre": "Sofía", "paterno": "Torres", "materno": "Vargas", "fecha_nacimiento": "1991-09-05", "carnet": "789123", "sexo": "F"},
    {"id": 7, "nombre": "Pedro", "paterno": "Ramírez", "materno": "Morales", "fecha_nacimiento": "1988-12-12", "carnet": "159753", "sexo": "M"},
    {"id": 8, "nombre": "Lucía", "paterno": "Flores", "materno": "Ortega", "fecha_nacimiento": "1995-04-18", "carnet": "357159", "sexo": "F"},
    {"id": 9, "nombre": "Jorge", "paterno": "Silva", "materno": "Reyes", "fecha_nacimiento": "1994-08-25", "carnet": "753951", "sexo": "M"},
    {"id": 10, "nombre": "Elena", "paterno": "Mendoza", "materno": "Castro", "fecha_nacimiento": "1997-06-14", "carnet": "852456", "sexo": "F"}
]

# Contador para generar IDs únicos (comenzará desde 11)
user_id_counter = 11

# API para crear un usuario
@app.route('/usuarios/crear', methods=['POST'])
def crear_usuario():
    global user_id_counter
    data = request.get_json()

    # Validar que todos los campos estén presentes
    campos_obligatorios = ['nombre', 'paterno', 'materno', 'fecha_nacimiento', 'carnet', 'sexo']
    if not all(campo in data for campo in campos_obligatorios):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Crear el nuevo usuario
    nuevo_usuario = {
        "id": user_id_counter,
        "nombre": data['nombre'],
        "paterno": data['paterno'],
        "materno": data['materno'],
        "fecha_nacimiento": data['fecha_nacimiento'],
        "carnet": data['carnet'],
        "sexo": data['sexo']
    }

    # Agregar el usuario a la fake DB
    usuarios.append(nuevo_usuario)
    user_id_counter += 1

    return jsonify(nuevo_usuario), 201

# API para listar todos los usuarios
@app.route('/usuarios/listar', methods=['POST'])
def listar_usuarios():
    return jsonify(usuarios), 200

# API para buscar un usuario por ID
@app.route('/usuarios/buscar', methods=['POST'])
def buscar_usuario():
    data = request.get_json()

    # Validar que el campo 'id' esté presente
    if 'id' not in data:
        return jsonify({"error": "El campo 'id' es obligatorio"}), 400

    # Buscar el usuario por ID
    user_id = data['id']
    usuario = next((user for user in usuarios if user['id'] == user_id), None)

    if usuario:
        return jsonify(usuario), 200
    else:
        return jsonify({"error": f"Usuario con ID {user_id} no encontrado"}), 404

# API para eliminar un usuario por ID
@app.route('/usuarios/eliminar', methods=['POST'])
def eliminar_usuario():
    data = request.get_json()

    # Validar que el campo 'id' esté presente
    if 'id' not in data:
        return jsonify({"error": "El campo 'id' es obligatorio"}), 400

    # Buscar y eliminar el usuario
    user_id = data['id']
    global usuarios
    usuarios = [user for user in usuarios if user['id'] != user_id]

    return jsonify({"mensaje": f"Usuario con ID {user_id} eliminado"}), 200

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Cliente publicador - IOP"})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
