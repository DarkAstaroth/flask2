from flask import jsonify 
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from db_client import Llaves, db

def cifrar_mensaje(mensaje, public_key_base64):
    try:
        public_key_pem = base64.b64decode(public_key_base64)
        public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
        key_simetrica = os.urandom(32)
        iv = os.urandom(16)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        mensaje_con_relleno = padder.update(mensaje.encode("utf-8")) + padder.finalize()
        cipher = Cipher(algorithms.AES(key_simetrica), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        mensaje_cifrado = encryptor.update(mensaje_con_relleno) + encryptor.finalize()
        clave_simetrica_cifrada = public_key.encrypt(
            key_simetrica,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return {
            "datos": base64.b64encode(mensaje_cifrado).decode("utf-8"),
            "clave_simetrica": base64.b64encode(clave_simetrica_cifrada).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
        }
    except Exception as e:
        return {"error": str(e)}

def descifrar_mensaje(datos_cifrados, clave_simetrica_cifrada, iv):
    try:
        llave = Llaves.query.first()
        if not llave:
            return jsonify(
                {
                    "error": "No se ha encontrado ninguna clave privada en la base de datos."
                }
            ), 404

        private_key_pem = base64.b64decode(llave.private_key.encode("utf-8"))
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  
            backend=default_backend(),
        )
        clave_simetrica = private_key.decrypt(
            base64.b64decode(clave_simetrica_cifrada),
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        cipher = Cipher(algorithms.AES(clave_simetrica), modes.CBC(base64.b64decode(iv)), backend=default_backend())
        decryptor = cipher.decryptor()
        mensaje_con_relleno = decryptor.update(base64.b64decode(datos_cifrados)) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        mensaje_descifrado = unpadder.update(mensaje_con_relleno) + unpadder.finalize()
        return {"mensaje_descifrado": mensaje_descifrado.decode("utf-8")}
    except Exception as e:
        return {"error": str(e)}