import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from db_client import Llaves, db

def generar_llaves_service():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    private_base64 = base64.b64encode(private_pem).decode("utf-8")
    public_base64 = base64.b64encode(public_pem).decode("utf-8")
    nueva_llave = Llaves(private_key=private_base64, public_key=public_base64)
    db.session.add(nueva_llave)
    db.session.commit()
    return {
        "id": nueva_llave.id,
        "private_key": private_base64,
        "public_key": public_base64,
        "fecha_creacion": nueva_llave.fecha_creacion.isoformat(),
    }

def obtener_llave_publica_service():
    llave = Llaves.query.first()
    if not llave:
        return {"error": "No se ha encontrado ninguna llave pública en la base de datos."}
    return {
        "public_key": llave.public_key,
        "fecha_creacion": llave.fecha_creacion.isoformat(),
    }