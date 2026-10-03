from app.database.db import Session
from app.repositories.login_repository import get_usuario_repository , post_usuario_repository
from app.security.login import comprobar_contrasena , hash_contrasena
from os import getenv


def comprobar_login_service(sesion : Session , usuario , contrasena):
    usuario_db = get_usuario_repository(sesion , usuario)
    if usuario_db is None:
        return {"ok" : False , "detail" : "Usuario o contraseña incorrectos"}
    elif not comprobar_contrasena(contrasena , usuario_db.contrasena_hasheada):
        return {"ok" : False , "detail" : "Usuario o contraseña incorrectos"}
    else:
        return {"ok" : True , "detail" : "Login correcto" , "usuario" : usuario_db}


def crear_primer_usuario_service(sesion : Session):
    usuario = "superuser"
    contrasena = getenv("SUPERUSER_PASSWORD")
    usuario_db = get_usuario_repository(sesion , usuario)
    if usuario_db is None and contrasena is not None:
        contrasena_hasheada = hash_contrasena(contrasena)
        post_usuario_repository(sesion , usuario , contrasena_hasheada)
    else:
        pass
