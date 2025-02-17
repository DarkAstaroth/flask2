from flask import Flask, jsonify, request
import os
import jwt
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from db_client import db, init_db, Llaves
import base64

def create_app():
    app = Flask(__name__)
    
    # Inicializar la base de datos
    init_db(app)

    # Crear tablas dentro del contexto de la aplicación
    with app.app_context():
        db.create_all()

    return app

app = create_app()

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

# Clave secreta para firmar los tokens JWT (en un entorno real, esto debería ser una clave segura y no estar hardcodeada)
SECRET_KEY = "supersecretkey"


# API para hacer el cifrado híbrido
@app.route('/cifrado-hibrido', methods=['POST'])
def cifrado_hibrido():
    try:
        # Recibir datos en el cuerpo de la solicitud
        data = request.get_json()
        mensaje = data['mensaje']
        public_key_base64 = data['public_key']

        # Decodificar la clave pública desde Base64 y cargarla
        public_key_pem = base64.b64decode(public_key_base64)
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

        # Generar clave simétrica AES de 256 bits
        key_simetrica = os.urandom(32)  # Clave simétrica de 256 bits
        iv = os.urandom(16)  # IV (Vector de Inicialización) para el cifrado AES

        # Cifrar el mensaje con AES-GCM (cifra el mensaje y genera un tag de autenticidad)
        cipher = Cipher(algorithms.AES(key_simetrica), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        mensaje_cifrado = encryptor.update(mensaje.encode('utf-8')) + encryptor.finalize()
        tag = encryptor.tag

        # Cifrar la clave simétrica (AES) con la clave pública RSA
        clave_simetrica_cifrada = public_key.encrypt(
            key_simetrica,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Enviar la respuesta con los datos cifrados
        return jsonify({
            "datos": base64.b64encode(mensaje_cifrado).decode('utf-8'),
            "clave_simetrica": base64.b64encode(clave_simetrica_cifrada).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "tag": base64.b64encode(tag).decode('utf-8')
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/descifrar', methods=['POST'])
def descifrar():
    try:
        # Recibir datos en el cuerpo de la solicitud
        data = request.get_json()
        datos_cifrados = base64.b64decode(data['datos'])
        clave_simetrica_cifrada = base64.b64decode(data['clave_simetrica'])
        iv = base64.b64decode(data['iv'])
        tag = base64.b64decode(data['tag'])

        # Obtener la clave privada de la base de datos
        llave = Llaves.query.first()
        if not llave:
            return jsonify({"error": "No se ha encontrado ninguna clave privada en la base de datos."}), 404

        # Convertir la clave privada de Base64 a formato PEM
        private_key_pem = base64.b64decode(llave.private_key.encode('utf-8'))

        # Cargar la clave privada
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  # Si la clave privada está cifrada, necesitas la contraseña
            backend=default_backend()
        )

        # Descifrar la clave simétrica con la clave privada RSA
        clave_simetrica = private_key.decrypt(
            clave_simetrica_cifrada,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Descifrar el mensaje con AES-GCM
        cipher = Cipher(algorithms.AES(clave_simetrica), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        mensaje_descifrado = decryptor.update(datos_cifrados) + decryptor.finalize()

        # Responder con el mensaje descifrado
        return jsonify({"mensaje_descifrado": mensaje_descifrado.decode('utf-8')}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API para generar un token JWT
@app.route('/generar-token', methods=['POST'])
def generar_token():
    # En un entorno real, aquí deberías validar las credenciales del usuario

    # Crear el token JWT
    token = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira en 1 hora
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({"token": token}), 200

# API para generar llaves públicas y privadas
@app.route('/generar-llaves', methods=['POST'])
def generar_llaves():
    # Verificar si ya existe una llave en la base de datos
    llave_existente = Llaves.query.first()

    # Si existe, eliminarla
    if llave_existente:
        db.session.delete(llave_existente)
        db.session.commit()

    # Generar nuevas llaves
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Codificar las llaves en base64
    private_base64 = base64.b64encode(private_pem).decode('utf-8')
    public_base64 = base64.b64encode(public_pem).decode('utf-8')

    # Crear nueva entrada en la base de datos
    nueva_llave = Llaves(private_key=private_base64, public_key=public_base64)
    db.session.add(nueva_llave)
    db.session.commit()

    return jsonify({
        "id": nueva_llave.id,
        "private_key": private_base64,
        "public_key": public_base64,
        "fecha_creacion": nueva_llave.fecha_creacion.isoformat()
    }), 200

@app.route('/llave-publica', methods=['GET'])
def obtener_llave_publica():
    # Buscar la llave pública almacenada en la base de datos
    llave = Llaves.query.first()

    # Si no hay ninguna llave generada, devolver un error
    if not llave:
        return jsonify({"error": "No se ha encontrado ninguna llave pública en la base de datos."}), 404

    # La llave pública ya está almacenada en Base64
    public_key_base64 = llave.public_key

    # Devolver la llave pública en Base64
    return jsonify({
        "public_key": public_key_base64,
        "fecha_creacion": llave.fecha_creacion.isoformat()
    }), 200


# Middleware para verificar el token JWT
def verificar_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except:
        return False

# API para listar todos los usuarios (requiere token)
@app.route('/usuarios/listar', methods=['POST'])
def listar_usuarios():
    # Obtener el token desde el header Authorization
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token no proporcionado o formato incorrecto"}), 401

    return jsonify(usuarios), 200

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
