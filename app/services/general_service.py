from app.database.db import Base , LocalSession , engine 
from pydantic import BaseModel 
from app.repositories.motivo_repository import conteo_motivos_db , post_motivo_db
from datetime import datetime


#SERVICIOS DE BASE DE DATOS#
def crear_db():
    Base.metadata.create_all(bind=engine)
def crear_primer_motivo():
    with LocalSession() as sesion :
            if conteo_motivos_db(sesion) == 0:
                post_motivo_db(sesion = sesion , motivo = "fichaje")
            elif conteo_motivos_db(sesion) != 0:
                pass
#SERVICIOS GENERALES #  
def limpiar_texto(texto : str | None)-> str:
    texto_limpio = texto.strip().lower()
    return texto_limpio
def datetime_a_str(fecha_hora : datetime )->str:
    strfecha = fecha_hora.strftime("%d-%m-%Y %H:%M:%S")
    return strfecha
def str_vacio_a_None(texto : str | None)->str | None:
    if len(texto) == 0 or texto is None  :
        return None
    else:
        return texto

        
        
    