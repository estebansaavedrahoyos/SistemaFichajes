from app.repositories.puesto_repository import get_puestos_db , post_puesto_db , verificar_existencia_puesto_db , delete_puesto_db
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

#GET SERVICES

def get_puestos_service(sesion : Session , puesto : None | str):
    try:
        if puesto is not None:
            if verificar_existencia_puesto_db(sesion , puesto) == True:
                lista_puestos = get_puestos_db(sesion , puesto )
                return [lista_puestos]
            elif verificar_existencia_puesto_db(sesion , puesto) == False:
                return {"detail" : f"No se ha encontrado el puesto {puesto}"}
        elif puesto is None:
            lista_puestos = get_puestos_db(sesion , None)
            return lista_puestos
    except SQLAlchemyError:
            return {"detail" : "Fallo en la base de datos , intentelo de nuevo"}

#POST SERVICES

def post_puesto_service(sesion:Session , puesto : str):
        try:
            if verificar_existencia_puesto_db(sesion , puesto) == False:
                post_puesto_db(sesion , puesto )
                return {"detail" : f"Puesto '{puesto}' añadido con exito" }
            elif verificar_existencia_puesto_db(sesion , puesto) == True :
                return {"detail" :f"El puesto '{puesto}' ya existe"}
        except SQLAlchemyError:
            return {"detail" : "Fallo en base de datos , intentelo de nuevo"}
    
        
    
#DELETE SERVICES 

def delete_puesto_service(sesion , puesto):
    
        try:
            if verificar_existencia_puesto_db(sesion , puesto) == True:
                delete_puesto_db(sesion , puesto)
                return {"detail" : f"Puesto '{puesto}' eliminado con exito" }
            elif verificar_existencia_puesto_db(sesion , puesto) == False:
                return {"detail" : f"El puesto '{puesto}' no existe"}
        except SQLAlchemyError:
            return {"detail":"Fallo en base de datos , intentelo de nuevo"}       
       