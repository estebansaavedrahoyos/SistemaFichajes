
from sqlalchemy import select , func , exists , delete 
from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import MotivosORM

#REPOSITORIOS GET 
def get_motivos_db(sesion : Session  , motivo : str | None):
    if motivo is None:
        return sesion.scalars(select(MotivosORM)).all()
    if motivo is not None :
        return sesion.scalar(select(MotivosORM).where(MotivosORM.motivo == motivo))

#REPOSITORIOS POST 

def post_motivo_db( sesion : Session , motivo : str):
    nuevo_motivo = MotivosORM(motivo = motivo )
    try:
        #raise SQLAlchemyError#RAISE PARA PROBAR ERRORES 
        sesion.add(nuevo_motivo)
        sesion.commit()
        sesion.refresh(nuevo_motivo)
    except SQLAlchemyError:
        sesion.rollback()
        raise 
    
#REPOSITORIOS DELETE 

def delete_motivo_db(sesion : Session , motivo : str):
    stmt = delete(MotivosORM).where(MotivosORM.motivo == motivo )
    try:
        #raise SQLAlchemyError#RAISE PARA PROBAR ERRORES 
        sesion.execute(stmt)
        sesion.commit()
    except SQLAlchemyError:
        sesion.rollback()
        raise
    
            
            
            

#REPOSITORIOS GENERALES Y DE VERIFICACION 

def conteo_motivos_db(sesion : Session):
        conteo = sesion.scalars(select(MotivosORM)).all()
        return len(conteo)
def verificar_existencia_motivo_db(sesion : Session , motivo : str ):
    #raise SQLAlchemyError#RAISE PARA PRUEBA DE ERRORES
    return sesion.scalar(select(exists().where(MotivosORM.motivo == motivo)))


