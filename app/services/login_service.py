from app.repositories.login_repository import get_hashed_contrasena_repository
from app.database.db import get_db  , Session
from fastapi import Depends
from typing import Annotated
def get_hashed_contrasena_service(sesion : Annotated[Session , Depends(get_db)] , usuario):
    return get_hashed_contrasena_repository(sesion , usuario)