from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.motivo_repository import get_motivos_db , post_motivo_db , verificar_existencia_motivo_db , delete_motivo_db

#GET SERVICES

def get_motivo_service(sesion : Session  , motivo : str | None):
    try:
        if motivo is not None:
            if verificar_existencia_motivo_db(sesion , motivo) == True:
                lista_motivos = get_motivo_service(sesion , motivo)
                return lista_motivos
            elif verificar_existencia_motivo_db(sesion , motivo) == False:
                return {"detail": f"No existe el puesto {motivo}"}
        elif motivo is None:
            lista_motivos = get_motivos_db(sesion , motivo )
            return lista_motivos
    except SQLAlchemyError:
        return {"detail":"Fallo en la base de datos , intentelo de nuevo"}
    
#POST SERVICES

def post_motivo_service(sesion :Session , motivo :str ):
    try:
        if verificar_existencia_motivo_db(sesion , motivo) == False:
            post_motivo_db(sesion , motivo)
            return {"detail" : f"Motivo '{motivo}' añadido con exito"}
        elif verificar_existencia_motivo_db(sesion , motivo) == True:
            return {"detail" : f"El motivo '{motivo}' ya existe"}
    except SQLAlchemyError as e:
        return {"detail":"Fallo en la base de datos , intentelo de nuevo"}
    
#DELETE SERVICES

def delete_motivo_service(sesion : Session , motivo : str):
    try:
        if verificar_existencia_motivo_db(sesion , motivo) == True:
            delete_motivo_db(sesion , motivo)
            return {"detail" : f"Motivo '{motivo}' borrado con exito"}
        elif verificar_existencia_motivo_db(sesion , motivo) == False:
            return {"detail" : f"No existe el motivo '{motivo}'"}
    except SQLAlchemyError:
        return {"detail":"Fallo en la base de datos , intentelo de nuevo"}
    
        
        
    

    
        
        
    
    