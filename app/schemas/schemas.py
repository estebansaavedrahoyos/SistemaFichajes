from pydantic import BaseModel , ConfigDict , Field , BeforeValidator ,  field_validator , AfterValidator
from fastapi import Query
from typing import Annotated , Literal
from datetime import datetime
from app.services.general_service import limpiar_texto  , datetime_a_str , str_vacio_a_None



### MODELOS DE RESPUESTA###
class RespuestaPuesto(BaseModel):
    id_puesto : Annotated[int , Field(validation_alias="id")]
    puesto : str
    model_config = ConfigDict(from_attributes=True)
    
class RespuestaMotivo(BaseModel):
    id_motivo : Annotated[int , Field(validation_alias="id")]
    motivo  : str
    model_config = ConfigDict(from_attributes=True)
class RespuestaEmpleado(BaseModel):
    id_empleado : Annotated[int , Field(validation_alias="id")]
    nombre : str
    puesto : Annotated[str , Field(validation_alias="nombre_puesto")]
            
            
        
    model_config = ConfigDict(from_attributes=True)
class RespuestaFichajes(BaseModel):
    id_fichaje : Annotated[int , Field(validation_alias="id")]
    fecha_hora : Annotated[datetime , AfterValidator(datetime_a_str)]
    tipo : str 
    nombre_empleado : str 
    puesto : Annotated[str , Field(validation_alias="puesto_empleado")]
    motivo : Annotated[str , Field(validation_alias="nombre_motivo")]
    model_config = ConfigDict(from_attributes=True)


##  MODELOS DE ENTRADA####

class PostEmpleado(BaseModel):
    nombre : Annotated[str , BeforeValidator(limpiar_texto)]
    puesto : Annotated[str  , BeforeValidator(limpiar_texto)]
    usuario : Annotated[str | None , BeforeValidator(limpiar_texto)] = None
    contrasena : str | None = None
    admin : bool = False
    
   
    
class FiltrosEmpleado(BaseModel):
    nombre : Annotated[str|None , Query() , BeforeValidator(limpiar_texto) ,
                                            AfterValidator(str_vacio_a_None)] = None
    puesto : Annotated[str|None , Query() , BeforeValidator(limpiar_texto) , 
                                            AfterValidator(str_vacio_a_None)] = None
    
class PostFichajes(BaseModel):
    
    nombre_empleado : Annotated[str , BeforeValidator(limpiar_texto)]
    motivo : Annotated[str , BeforeValidator(limpiar_texto) ] = "fichaje"
    

class FiltrosFichajes(BaseModel):
    
    @field_validator("fecha" , "tipo" , "nombre_empleado" , "puesto_empleado" , "motivo" , mode= "after")
    @classmethod
    def limpiar_texto_fichajes(cls , texto : str | None)->str | None:
        if texto is None:
            return None
        elif isinstance(texto , str):
            return limpiar_texto(texto) 
        
    fecha : str | None = None
    tipo : Literal["entrada" , "salida" ] | None = None 
    nombre_empleado : str | None = None
    puesto_empleado : str | None = None
    motivo : str |None = None
    
    
    
        
    
    
    
    
    
    

    