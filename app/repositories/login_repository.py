from app.database.db import get_db  , Session
from fastapi import Depends
from typing import Annotated
from sqlalchemy import select
from app.models.models import UsuariosORM

def get_hashed_contrasena_repository( sesion : Session , usuario):
    return sesion.scalar(select(UsuariosORM.contrasena_hasheada).where(usuario == ))