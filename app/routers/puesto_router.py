from fastapi import APIRouter , Depends , Query , HTTPException
from typing import List , Annotated 
from pydantic import Field , AfterValidator , BeforeValidator , ValidationInfo
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session 
from app.schemas.schemas import RespuestaPuesto
from app.database.db import get_db
from app.services.puesto_service import get_puestos_service , post_puesto_service , delete_puesto_service
from app.services.general_service import limpiar_texto


router = APIRouter(tags=["Puestos"])

@router.get("/puestos_api" , response_model= List[RespuestaPuesto])
def get_puestos_router(sesion : Annotated [ Session, Depends(get_db) ]):
    return get_puestos_service(sesion)
    
@router.post("/puestos_api")
def post_puesto_router(sesion : Annotated[Session , Depends(get_db)] , puesto : Annotated[str , Query(min_length=3 ),
                                                                                     BeforeValidator(limpiar_texto)]):
    return post_puesto_service(sesion , puesto) 
@router.delete("/puestos_api")
def delete_puesto_router(sesion : Annotated[Session , Depends(get_db)] , puesto : Annotated[str ,
                                                                        BeforeValidator(limpiar_texto)]): 
    return delete_puesto_service(sesion , puesto)
        