from app.database.db import Session
from sqlalchemy import select
from app.models.models import UsuariosORM , EmpleadosORM


def get_usuario_repository(sesion : Session , usuario):
    return sesion.scalar(select(UsuariosORM).where(UsuariosORM.usuario == usuario))


def post_usuario_repository(sesion : Session , usuario , contrasena_hasheada):
    empleado = EmpleadosORM(nombre = usuario , admin = True)
    sesion.add(empleado)
    sesion.flush()
    nuevo_usuario = UsuariosORM(usuario = usuario , contrasena_hasheada = contrasena_hasheada , id_empleado = empleado.id)
    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)
    return nuevo_usuario
