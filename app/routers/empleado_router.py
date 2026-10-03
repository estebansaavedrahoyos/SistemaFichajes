from fastapi import APIRouter , Depends , Query 
from typing import Annotated , List 
from pydantic import BeforeValidator
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.schemas import PostEmpleado
from app.services.empleado_service import post_empleado_service , get_empleado_service , delete_empleado_service
from app.services.general_service import limpiar_texto
from app.schemas.schemas import RespuestaEmpleado , FiltrosEmpleado

router = APIRouter(tags=["Empleados"])
@router.get("/empleados_api" , response_model = List[RespuestaEmpleado])
def get_empleados_router(sesion : Annotated[Session , Depends(get_db)] , filtros : Annotated[None, Query(include_in_schema=False) ]= None):
    return get_empleado_service(sesion , filtros )

@router.get("/empleados_filtro_api" , response_model=List[RespuestaEmpleado])
def get_empelados_filtro_router(sesion : Annotated[Session , Depends(get_db)] , filtros : Annotated[FiltrosEmpleado , Query()]):
    return get_empleado_service(sesion , filtros)


@router.post("/post_empleado_api")
def post_empleado_router(sesion : Annotated[Session , Depends(get_db)] , empleado : PostEmpleado):
    return post_empleado_service(sesion , empleado)

@router.delete("/delete_empleado_api")
def delete_empleado_router(sesion : Annotated[Session , Depends(get_db)] , nombre : Annotated[str , Query() , BeforeValidator(limpiar_texto)],
                    puesto : Annotated[str , Query() , BeforeValidator(limpiar_texto)]):
    return delete_empleado_service(sesion , nombre , puesto)
    