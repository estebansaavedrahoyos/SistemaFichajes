from fastapi import APIRouter , Depends , Query , HTTPException 
from pydantic import BeforeValidator
from typing import List , Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schemas import RespuestaMotivo
from app.services.general_service import limpiar_texto
from app.database.db import get_db
from app.services.motivo_service import get_motivo_service , post_motivo_service , delete_motivo_service


router = APIRouter(tags=["Motivos"])


@router.get("/motivos_api" , response_model= List[RespuestaMotivo])
def get_motivos_router(sesion : Annotated[Session , Depends(get_db)] ):
    return get_motivo_service(sesion)
    
@router.post("/motivos_api")
def post_motivo_router(sesion : Annotated[Session , Depends(get_db)] , motivo : Annotated[str , Query(min_length=3),
                                                                                    BeforeValidator(limpiar_texto)]):
    return post_motivo_service(sesion , motivo)

@router.delete("/motivos_api")
def delete_post_router(sesion : Annotated[Session , Depends(get_db)] , motivo : Annotated[str , Query() , 
                                                                            BeforeValidator(limpiar_texto)]):
    return delete_motivo_service(sesion , motivo)
