usuarios = [
    # Lista de usuarios
]

def listar_usuarios_service():
    return usuarios

def crear_usuario_service(data):
    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": data["nombre"],
        "paterno": data["paterno"],
        "materno": data["materno"],
        "fecha_nacimiento": data["fecha_nacimiento"],
        "carnet": data["carnet"],
        "sexo": data["sexo"],
    }
    usuarios.append(nuevo_usuario)
    return nuevo_usuario

def buscar_usuario_service(user_id):
    usuario = next((user for user in usuarios if user["id"] == user_id), None)
    return usuario if usuario else {"error": f"Usuario con ID {user_id} no encontrado"}

def eliminar_usuario_service(user_id):
    global usuarios
    usuarios = [user for user in usuarios if user["id"] != user_id]
    return {"mensaje": f"Usuario con ID {user_id} eliminado"}