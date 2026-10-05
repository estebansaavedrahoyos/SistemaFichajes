from app.models.models import EmpleadosORM , PuestosORM
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select , exists , delete
from typing import Annotated, List

#REPOSITORIOS GET 
def get_empleado_db(sesion : Session , filtros : List | None = None):
    if filtros is None:
        return sesion.scalars(select(EmpleadosORM)).all()
    else:
        return  sesion.scalars(select(EmpleadosORM).join(PuestosORM , PuestosORM.id == EmpleadosORM.id_puesto).where(*filtros)).all()
        
    
#REPOSITORIOS POST#

def post_empleado_db(sesion : Session  , nombre_empleado : str , id_puesto : int , admin : bool = False):
    nuevo_empleado = EmpleadosORM(nombre = nombre_empleado , id_puesto = id_puesto , admin = admin)
    try: 
        sesion.add(nuevo_empleado)
        sesion.commit()
        sesion.refresh(nuevo_empleado)
        return nuevo_empleado
    except SQLAlchemyError:
        sesion.rollback()
        raise
    


#REPOSITORIOS DELETE#

def delete_empleado_db(sesion : Session , nombre : str , puesto : str):
    try:
        stmt = sesion.scalar(select(EmpleadosORM).join(PuestosORM , PuestosORM.id == EmpleadosORM.id_puesto).where(EmpleadosORM.nombre == nombre , PuestosORM.puesto == puesto))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<",stmt)
        sesion.delete(sesion.scalar(select(EmpleadosORM).join(PuestosORM , PuestosORM.id == EmpleadosORM.id_puesto).where(EmpleadosORM.nombre == nombre , PuestosORM.puesto == puesto)))
        sesion.commit()
    except SQLAlchemyError:
        sesion.rollback()
        raise
        

#REPOSITORIOS GENERALES#

def verificar_existencia_empleado_db(sesion : Session , nombre : str , puesto : str | None = None):
    if puesto:
        return sesion.scalar(select(exists().where(EmpleadosORM.nombre == nombre )))
    elif puesto is None:
        return sesion.scalar(select(exists().where(EmpleadosORM.nombre == nombre )))
    
   