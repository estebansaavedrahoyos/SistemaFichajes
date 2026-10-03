from fastapi import APIRouter , Depends , Query
from pydantic import BeforeValidator
from app.database.db import get_db  , Session
from app.services.general_service import limpiar_texto
from app.services.fichaje_service import get_fichajes_service, post_fichajes_service
from app.schemas.schemas import RespuestaFichajes , FiltrosFichajes , PostFichajes
from typing import List , Annotated 
from datetime import datetime

router = APIRouter(tags=["Fichajes"])

@router.get("/ultimos_fichajes" , response_model=list[RespuestaFichajes])
def get_fichajes_router(sesion : Annotated[Session , Depends(get_db)]):
    return get_fichajes_service(sesion , filtros = None )


@router.get("/busqueda_fichajes" , response_model=list[RespuestaFichajes])
def get_fichajes_filtros_router(sesion : Annotated[Session , Depends(get_db)] , filtros :Annotated[FiltrosFichajes , Query()]):
    return get_fichajes_service(sesion , filtros)

@router.post("/nuevo_fichaje_2")
def post_fichajes_router(sesion : Annotated[Session , Depends(get_db)] , fichaje : PostFichajes):
    fecha_hora = datetime.now()
    return post_fichajes_service(sesion , fichaje , fecha_hora)