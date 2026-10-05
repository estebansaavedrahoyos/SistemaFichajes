from app.database.db import Session
from sqlalchemy import select
from app.models.models import UsuariosORM , EmpleadosORM , PuestosORM


def get_usuario_repository(sesion : Session , usuario):
    return sesion.scalar(select(UsuariosORM).where(UsuariosORM.usuario == usuario))


def post_usuario_repository(sesion : Session , usuario , contrasena_hasheada):
    id_puesto_admin = sesion.scalar(select(PuestosORM.id).where(PuestosORM.puesto == "admin"))
    empleado = EmpleadosORM(nombre = usuario , id_puesto = id_puesto_admin , admin = True)
    sesion.add(empleado)
    sesion.flush()
    nuevo_usuario = UsuariosORM(usuario = usuario , contrasena_hasheada = contrasena_hasheada , id_empleado = empleado.id)
    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)
    return nuevo_usuario


def post_usuario_empleado_repository(sesion : Session , usuario , contrasena_hasheada , id_empleado):
    nuevo_usuario = UsuariosORM(usuario = usuario , contrasena_hasheada = contrasena_hasheada , id_empleado = id_empleado)
    sesion.add(nuevo_usuario)
    sesion.commit()
    sesion.refresh(nuevo_usuario)
    return nuevo_usuario
