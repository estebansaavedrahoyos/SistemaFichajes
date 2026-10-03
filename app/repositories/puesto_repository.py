from app.database.db import Session 
from app.models.models import PuestosORM , EmpleadosORM
from sqlalchemy import select , exists , delete 
from sqlalchemy.exc import SQLAlchemyError 

#REPOSITORIOS GET#

def get_puestos_db(sesion : Session , puesto : None | str ):
    #raise SQLAlchemyError#RAISE PARA PRUEBA DE ERRORES EN BD 
    if puesto is None:  
        return sesion.scalars(select(PuestosORM)).all()
    elif puesto is not None:
        return sesion.scalar(select(PuestosORM).where(PuestosORM.puesto == puesto))
        
        

#REPOSITORIOS POST#
def post_puesto_db(sesion : Session , puesto : str):
    nuevo_puesto = PuestosORM(puesto = puesto )
    try:
        #raise SQLAlchemyError#RAISE PARA PRUEBA DE ERRORES EN BD
        sesion.add(nuevo_puesto)
        sesion.commit()
        sesion.refresh(nuevo_puesto)
    except SQLAlchemyError:
        sesion.rollback()
        raise 
#REPOSITORIOS DELETE#
def delete_puesto_db(sesion : Session , puesto : str):
    stmt = delete(PuestosORM).where(PuestosORM.puesto == puesto)
    try:
        #raise SQLAlchemyError#RAISE PARA PRUEBA DE ERRORES EN BD
        sesion.execute(stmt)
        sesion.commit()
    except SQLAlchemyError:
        sesion.rollback()
        raise 
    
#REPOSITORIOS GENERALES Y DE VERIFICACION #
def verificar_existencia_puesto_db(sesion : Session , puesto):
    #raise SQLAlchemyError #RAISE PARA PRUEBA DE ERRORES EN DB
    return sesion.scalar(select(exists().where(PuestosORM.puesto == puesto)))

def id_puesto_desde_puesto(sesion : Session, puesto):
    return sesion.scalar(select(PuestosORM.id).where(PuestosORM.puesto == puesto))
  
    