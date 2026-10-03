from app.database.db import Session
from app.schemas.schemas import FiltrosFichajes
from app.models.models import FichajesORM , EmpleadosORM , MotivosORM , PuestosORM
from sqlalchemy import select , func , desc
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


#REPOSITORIOS GET#

def get_fichajes_db(sesion : Session , filtros : list | None):
    if filtros is None: 
        return sesion.scalars(select(FichajesORM ).order_by(desc(FichajesORM.id)).limit(30)).all()
    elif filtros is not None:
        return sesion.scalars(select(FichajesORM).join(EmpleadosORM , EmpleadosORM.id == FichajesORM.id_empleado )
                              .join(MotivosORM , MotivosORM.id == FichajesORM.id_motivo)
                              .join(PuestosORM , PuestosORM.id == EmpleadosORM.id_puesto ).where(*filtros).order_by(desc(FichajesORM.id))).all()
#REPOSITORIOS POST#

def post_fichajes_db(sesion : Session , fichaje : FichajesORM):
    try:
        sesion.add(fichaje)
        sesion.commit()
    except SQLAlchemyError:
        sesion.rollback()
        raise
    
    
#REPOSITORIOS GENERALES  #
def id_empleado_por_nombre_db(sesion : Session , nombre_empleado : str):
    return sesion.scalar(select(EmpleadosORM.id).where(EmpleadosORM.nombre == nombre_empleado))

def id_motivo_por_nombre_db(sesion : Session , motivo : str):
    return sesion.scalar(select(MotivosORM.id).where(MotivosORM.motivo == motivo))
    
def calcular_tipo_db(sesion : Session , id_motivo : int , id_empleado : int): 
    calculo = sesion.scalar(select(func.count()).select_from(FichajesORM).where(FichajesORM.id_motivo == id_motivo ,
                                                                                FichajesORM.id_empleado == id_empleado ))
    if calculo %2 == 0:
        return "entrada"
    elif calculo %2 != 0:
        return "salida"