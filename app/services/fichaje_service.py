from app.database.db import Session 
from app.schemas.schemas import FiltrosFichajes , PostFichajes
from app.repositories.fichaje_repository import get_fichajes_db , id_empleado_por_nombre_db , id_motivo_por_nombre_db , calcular_tipo_db , post_fichajes_db
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated
from app.services.general_service import str_vacio_a_None
from pydantic import BeforeValidator
from fastapi import HTTPException
from datetime import datetime , timedelta , time , date
from app.models.models import FichajesORM , EmpleadosORM , MotivosORM , PuestosORM
from app.repositories.motivo_repository import verificar_existencia_motivo_db
from app.repositories.empleado_repository import verificar_existencia_empleado_db


#SERVICIONS GET#

def get_fichajes_service(sesion : Session  , filtros : FiltrosFichajes | None):     
    if filtros is None:
        try:
            lista_fichajes = get_fichajes_db(sesion , filtros)
            if len(lista_fichajes) <= 0:
                return { "detail" : "No se han encontrado ningun fichaje con estos filtros"}
            if len(lista_fichajes) >= 1:
                return lista_fichajes
        except SQLAlchemyError:
            raise HTTPException(status_code=404 , detail="Fallo en la base de datos intentelo de nuevo")
    elif filtros is not None:
        lista_filtros = filtros_fichaje_a_expresion_orm(sesion , filtros)
        try:
            lista_fichajes = get_fichajes_db(sesion , lista_filtros)
            if len(lista_fichajes) <= 0:
                return {"detail" :"No se ha encontrado ningun fichaje con estos filtros"}
            if len(lista_fichajes) >= 1:
                return lista_fichajes
        except SQLAlchemyError:
            raise HTTPException(status_code=404 , detail="Fallo en la base de datos intentelo de nuevo")
    
#SERVICIOS POST #
def post_fichajes_service(sesion : Session , fichaje : PostFichajes , fecha_hora : datetime ):
    nombre_empleado = fichaje.nombre_empleado
    motivo= str_vacio_a_None(fichaje.motivo)
    if motivo is None:
        motivo = "fichaje"
    try:
        if verificar_existencia_empleado_db(sesion , nombre_empleado) and verificar_existencia_motivo_db(sesion , motivo):
            id_empleado = id_empleado_por_nombre_db(sesion , nombre_empleado)
            id_motivo = id_motivo_por_nombre_db(sesion , motivo)
            tipo = calcular_tipo_db(sesion , id_motivo , id_empleado)
            fichaje_orm = FichajesORM(fecha_hora = fecha_hora , id_empleado = id_empleado 
                                      , id_motivo = id_motivo , tipo = tipo)
            post_fichajes_db(sesion , fichaje_orm)
            return {"detail" : "Fichaje creado con exito"}
        else: 
            return {"detail":"Empleado o motivo no existente"}
    except SQLAlchemyError as e:
        return {"detail":"Error en la base de datos intenterlo de nuevo "}
    
    

#SERVICIOS GENERALES#
def crear_datetime_desde_formato_espanol(fecha : str | None):
    if fecha is None:
        return None
    elif fecha is not None:
        fecha = fecha.split("/")
        fecha = [fecha[2] , fecha[1] , fecha[0]]
        fecha = datetime.combine(date(*map(int , fecha)), time(0,0,0,1))
        return fecha
def crear_intervalo_fechas(fecha : datetime):
    fecha_inicio = fecha
    fecha_final = fecha + timedelta(days=1)
    return (fecha_inicio , fecha_final)

#SERVICIOS FILTROS
def filtros_fichaje_a_expresion_orm(sesion : Session , filtros : FiltrosFichajes):
    dic_filtros = filtros.model_dump(exclude_none=True)
    lista_filtros = []
    if "fecha" in dic_filtros:
        datetime_filtro = crear_datetime_desde_formato_espanol(dic_filtros["fecha"])
        fecha_inicio , fecha_final = crear_intervalo_fechas(datetime_filtro)
        lista_filtros.append(FichajesORM.fecha_hora >= fecha_inicio)
        lista_filtros.append(FichajesORM.fecha_hora <= fecha_final)
    if "tipo" in dic_filtros:
        lista_filtros.append(FichajesORM.tipo == dic_filtros["tipo"])
    if "motivo" in dic_filtros:
        lista_filtros.append(MotivosORM.motivo == dic_filtros["motivo"])
    if "nombre_empleado" in dic_filtros:
        lista_filtros.append(EmpleadosORM.nombre == dic_filtros["nombre_empleado"])
    if "puesto_empleado" in dic_filtros:
        lista_filtros.append(PuestosORM.puesto == dic_filtros["puesto_empleado"])
    
    return lista_filtros 
def comprobar_fecha_correcta(dia : int | str , mes : int|str , año : int|str ) -> None | str | dict:
        if all([isinstance(dia , int) and dia >0 and dia <32 ,
               isinstance(mes , int) and mes >0 and mes < 13 ,
               isinstance(año , int) and año >0]):
           return f"{dia}/{mes}/{año}"
            
        elif all([dia is None or dia == "", mes is None or mes == "" , año is None or año == ""]):
            return None 
        else :
            return {"detail" : "Fecha no valida!! la fecha no puede ser negativa y deben de rellenarse todo (DIA MES Y AÑO) con el formato (31/12/2026)"}

    
        
