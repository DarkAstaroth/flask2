import jwt
import datetime

def generar_token():
    token = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        "supersecretkey",  # Usar la clave secreta desde .env
        algorithm="HS256",
    )
    return token

def verificar_token(token):
    try:
        jwt.decode(token, "supersecretkey", algorithms=["HS256"])
        return True
    except:
        return False