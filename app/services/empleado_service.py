from fastapi import HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schemas import PostEmpleado , FiltrosEmpleado
from app.repositories.puesto_repository import verificar_existencia_puesto_db , id_puesto_desde_puesto
from app.repositories.empleado_repository import post_empleado_db , get_empleado_db , delete_empleado_db , verificar_existencia_empleado_db
from app.repositories.login_repository import get_usuario_repository , post_usuario_empleado_repository
from app.security.login import hash_contrasena
from app.models.models import EmpleadosORM , PuestosORM

#GET SERVICIOS#


def get_empleado_service(sesion : Session , filtros : None | FiltrosEmpleado):
    if filtros is None:
        try:
            return get_empleado_db(sesion)
        except SQLAlchemyError:
            return {"detail":"Fallo en la base de datos , intentelo de nuevo "}
    elif filtros is not None :
        try:
            lista_empleados = get_empleado_db(sesion=sesion , filtros = filtros_empleado_a_expresion_orm(filtros))
            if len(lista_empleados) >= 1:
                return lista_empleados
            else:
                return {"detail" : "No se encontro un empleado con esos filtros "}
        except SQLAlchemyError:
            return {"detail":"Fallo en la base de datos , intentelo de nuevo "}
    
#POST SERVICIOS#

def post_empleado_service(sesion : Session  , empleado : PostEmpleado):
    try:
        if len(empleado.nombre) < 2:
            return {"detail" : "El nombre del empleado debe de tener al menos dos caracteres"}
        if verificar_existencia_empleado_db(sesion , empleado.nombre ) == True:
            return{"detail" : f"El empleado con nombre '{empleado.nombre}' ya existe"}
        elif verificar_existencia_empleado_db(sesion , empleado.nombre ) == False:
            if verificar_existencia_puesto_db(sesion , empleado.puesto) == True:
                id_puesto = id_puesto_desde_puesto(sesion , empleado.puesto)
                empleado_db = post_empleado_db(sesion , nombre_empleado=empleado.nombre , id_puesto = id_puesto , admin = empleado.admin)
                if empleado.usuario is not None and empleado.contrasena is not None and empleado.usuario != "" and empleado.contrasena != "":
                    if get_usuario_repository(sesion , empleado.usuario) is None:
                        post_usuario_empleado_repository(sesion , empleado.usuario , hash_contrasena(empleado.contrasena) , empleado_db.id)
                        return {"detail" : f"Empleado '{empleado.nombre}' con puesto '{empleado.puesto}' y usuario '{empleado.usuario}' , añadido con exito"}
                    else:
                        return {"detail" : f"Empleado creado pero el usuario '{empleado.usuario}' ya existe"}
                return {"detail" : f"Empleado '{empleado.nombre}' con puesto '{empleado.puesto}' , añadido con exito"}
            elif verificar_existencia_puesto_db(sesion , empleado.puesto) == False:
                return {"detail":f"El puesto '{empleado.puesto}' no es un puesto valido"}
        
        

    except SQLAlchemyError:
        return {"detail":"Fallo en la base de datos , intentelo de nuevo"}
    
#SERVICIOS DELETE#

def delete_empleado_service(sesion : Session , nombre : str , puesto : str):
    try:
        if verificar_existencia_empleado_service(sesion , nombre , puesto) == True:
            delete_empleado_db(sesion , nombre , puesto )
            return {"detail" : "Empleado eliminado con exito "}
        elif verificar_existencia_empleado_service(sesion , nombre , puesto) == False:
            return {"detail":f"No se ha encontrado el empleado '{nombre}' con puesto '{puesto}'"}
    except SQLAlchemyError as e:
        print("<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<",e)
        return {"detail":"Fallo en la base de datos , intentelo mas tarde"}
        

        
            
            
    
    
#SERIVCIO FILTROS#
def filtros_empleado_a_expresion_orm(filtros : FiltrosEmpleado)->list:
        lista_filtros = []
        dic_filtros = filtros.model_dump(exclude_none=True)
        if "nombre" in dic_filtros:
            lista_filtros.append(EmpleadosORM.nombre == dic_filtros["nombre"])
        if "puesto" in dic_filtros:
            lista_filtros.append(PuestosORM.puesto == dic_filtros["puesto"])
        if len(lista_filtros) >= 1:
            return lista_filtros
        if len(lista_filtros) == 0:
            raise HTTPException(status_code=404 , detail="Se necesita almenos un filtro de busqueda")

#SERVICIOS GENERALES #

def verificar_existencia_empleado_service(sesion : Session , nombre : str , puesto : str) -> bool:
    comprobacion = verificar_existencia_empleado_db(sesion , nombre , puesto)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><",comprobacion)
    return comprobacion
    
        
            