from fastapi import APIRouter, Request
from datetime import datetime
from pydantic import BeforeValidator , AfterValidator 
from app.schemas.schemas import FiltrosFichajes , FiltrosEmpleado , PostFichajes , PostEmpleado
from fastapi import Depends , Form , Query
from app.services.general_service import str_vacio_a_None , limpiar_texto
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.fichaje_service import get_fichajes_service , post_fichajes_service , comprobar_fecha_correcta
from app.services.empleado_service import get_empleado_service , post_empleado_service , delete_empleado_service
from app.services.puesto_service import get_puestos_service , post_puesto_service , delete_puesto_service
from app.services.motivo_service import get_motivo_service , post_motivo_service , delete_motivo_service
from app.services.login_service import comprobar_login_service
from app.database.db import Session , get_db
from typing import Annotated , Literal

router = APIRouter(tags=["Frontend"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request , sesion : Annotated[Session , Depends(get_db)] ):
    return templates.TemplateResponse(request=request,name="login.html",
        context={
            "lista_fichajes" : get_fichajes_service(sesion , None)
        }
    )
@router.post("/nuevo_fichaje" , response_class=HTMLResponse )
def nuevo_fichaje( request : Request,sesion : Annotated[Session , Depends(get_db)] , fichaje : Annotated[PostFichajes , Form()]):
    fecha_hora = datetime.now()
    diccionario_respuesta = {"lista_fichajes" : get_empleado_service(sesion , filtros=None)}
    post_fichaje = post_fichajes_service(sesion ,fichaje,fecha_hora)
    if "detail" in post_fichaje:
            diccionario_respuesta["info"] = post_fichaje["detail"]
    return templates.TemplateResponse(request=request,name="home.html",
        context={
            "lista_fichajes" : get_fichajes_service(sesion , None)
        })

@router.get("/fichajes" , response_class=HTMLResponse)
def fichajes(request : Request , sesion : Annotated[Session , Depends(get_db)],
              nombre_empleado : Annotated [str | None, Query() , BeforeValidator(str_vacio_a_None)] = None,
              puesto_empleado : Annotated[str | None , Query() , BeforeValidator(str_vacio_a_None)] = None,
              tipo : Annotated[Literal["entrada" , "salida" , "(opcional)"] | None , Query() , BeforeValidator(str_vacio_a_None) , BeforeValidator(limpiar_texto)] = None,
              motivo : Annotated[str | None , Query() , BeforeValidator(str_vacio_a_None)] = None,
              dia : Annotated[int|str | None , Query()] = None,
              mes : Annotated[int | str | None , Query()] = None,
              año : Annotated[int | str | None , Query()] = None):
    
    if tipo == "(opcional)":
        tipo = None
    diccionario_respuesta = {}  
    fecha = comprobar_fecha_correcta(dia , mes , año)
    if isinstance(fecha,dict):
            diccionario_respuesta["info"] = fecha["detail"]
            fecha = None
    
    filtros = FiltrosFichajes(fecha=fecha , tipo=tipo , nombre_empleado=nombre_empleado , puesto_empleado=puesto_empleado,
                                        motivo=motivo)

    lista_fichajes = get_fichajes_service(sesion , filtros) 
    
    if isinstance(lista_fichajes,dict):
        diccionario_respuesta["info"] = lista_fichajes["detail"]  
        diccionario_respuesta["lista_fichajes"] = get_fichajes_service(sesion , None)
    else:
        diccionario_respuesta["lista_fichajes"] = get_fichajes_service(sesion , filtros)
    
    return templates.TemplateResponse(request=request , name="fichajes.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })


    
@router.get("/empleados" , response_class=HTMLResponse)
def empleados(request : Request , sesion : Annotated[Session , Depends(get_db)] , filtros : Annotated[FiltrosEmpleado , Query()]):
    if all(filtro is None or filtro == "" for filtro in filtros.model_dump().values()):
        filtros = None
    diccionario_respuesta = {"lista_empleados" : get_empleado_service(sesion , filtros)}
    if "detail" in diccionario_respuesta["lista_empleados"]:
        diccionario_respuesta["info"] = diccionario_respuesta["lista_empleados"]["detail"]
        diccionario_respuesta["lista_empleados"] = get_empleado_service(sesion , None)
        
    return templates.TemplateResponse(request=request , name = "empleados.html",
                                      context={ 
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.post("/nuevo_empleado" ,response_class=HTMLResponse)
def nuevo_empleado(request : Request , sesion : Annotated[Session , Depends(get_db)] ,
                   empleado : Annotated[PostEmpleado , Form()]):
    
    return templates.TemplateResponse(request=request , name="empleados.html",
                                      context={
                                          "diccionario_respuesta" :  {"info" : post_empleado_service(sesion , empleado)["detail"],
                                                                      "lista_empleados" : get_empleado_service(sesion , None) ,}
                                          })
@router.post("/eliminar_empleado" , response_class=HTMLResponse)
def eliminar_empleado(request : Request , sesion : Annotated[Session , Depends(get_db)] ,
                      nombre : Annotated[str , Form() , BeforeValidator(limpiar_texto)] = None,
                      puesto : Annotated[str , Form() , BeforeValidator(limpiar_texto)] = None):
    diccionario_respuesta = {}
    if all([nombre , puesto]):
        diccionario_respuesta["info"] = delete_empleado_service(sesion , nombre , puesto)["detail"]
        diccionario_respuesta["lista_empleados"] = get_empleado_service(sesion , None)
        
    elif any([nombre == "" or nombre is None , puesto == "" or puesto is None]):
        diccionario_respuesta["lista_empleados"] = get_empleado_service(sesion , None)
        diccionario_respuesta["info"] = "Tanto empleado como puesto son campos obligatorios para eliminar"
    return templates.TemplateResponse(request=request , name="empleados.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.get("/puestos" , response_class=HTMLResponse)
def puestos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , puesto : Annotated[str | None , Query() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    diccionario_respuesta = {"lista_puestos" : get_puestos_service(sesion , puesto)}
    if "detail" in diccionario_respuesta["lista_puestos"]:
        diccionario_respuesta["info"] = diccionario_respuesta["lista_puestos"]["detail"]
        diccionario_respuesta["lista_puestos"] = get_puestos_service(sesion , None)      
    return templates.TemplateResponse(request=request , name="puestos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.post("/nuevo_puestos" , response_class=HTMLResponse)
def puestos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , puesto : Annotated[str | None , Form() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    if len(puesto) < 2:
        diccionario_respuesta = {"info" : "El puesto debe tener almenos dos caracteres",
                                     "lista_puestos" : get_puestos_service(sesion , None)}
    else:          
        diccionario_respuesta = {"info" : post_puesto_service(sesion , puesto)["detail"] ,
                             "lista_puestos" : get_puestos_service(sesion , None)}
    
    return templates.TemplateResponse(request=request , name="puestos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.post("/eliminar_puestos" , response_class=HTMLResponse)
def puestos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , puesto : Annotated[str | None , Form() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    diccionario_respuesta = {"info" : delete_puesto_service(sesion , puesto)["detail"] ,
                             "lista_puestos" : get_puestos_service(sesion , None)}
    return templates.TemplateResponse(request=request , name="puestos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.get("/motivos" , response_class=HTMLResponse)
def motivos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , motivo : Annotated[str | None , Query() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    diccionario_respuesta = {"lista_motivos" : get_motivo_service(sesion , motivo)} 
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" , diccionario_respuesta["lista_motivos"])
    if "detail" in diccionario_respuesta["lista_motivos"]:
        diccionario_respuesta["info"] = diccionario_respuesta["lista_motivos"]["detail"]
        diccionario_respuesta["lista_motivos"] = get_motivo_service(sesion , None)  
       
    return templates.TemplateResponse(request=request , name="motivos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.post("/nuevo_motivos" , response_class=HTMLResponse)
def post_puestos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , motivo : Annotated[str | None , Form() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    if len(motivo) < 2:
        diccionario_respuesta = {"info" : "El motivo debe tener almenos dos caracteres",
                                     "lista_motivos" : get_motivo_service(sesion , None)}
    else:          
        diccionario_respuesta = {"info" : post_motivo_service(sesion , motivo)["detail"] ,
                             "lista_motivos" : get_motivo_service(sesion , None)}
    
    return templates.TemplateResponse(request=request , name="motivos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })
@router.post("/eliminar_motivos" , response_class=HTMLResponse)
def delete_puestos(request : Request , sesion : Annotated[ Session , Depends(get_db)] , motivo : Annotated[str | None , Form() ,
                                                                                BeforeValidator(limpiar_texto) , 
                                                                                BeforeValidator(str_vacio_a_None) ] = None):
    diccionario_respuesta = {"info" : delete_motivo_service(sesion , motivo)["detail"] ,
                             "lista_motivos" : get_motivo_service(sesion , None)}
    return templates.TemplateResponse(request=request , name="motivos.html",
                                      context={
                                          "diccionario_respuesta" : diccionario_respuesta
                                      })   
        
@router.post("/login" , response_class=HTMLResponse)
def comprobar_login(request : Request , sesion : Annotated[Session , Depends(get_db)] ,
                    usuario : Annotated[str , Form()] , contrasena : Annotated[str , Form()]):
    resultado_login = comprobar_login_service(sesion , usuario , contrasena)
    if resultado_login["ok"] == False:
        return templates.TemplateResponse(request=request , name="login.html",
                                          context={
                                              "info" : resultado_login["detail"] ,
                                              "lista_fichajes" : get_fichajes_service(sesion , None)
                                          })
    else:
        return templates.TemplateResponse(request=request , name="home.html",
                                          context={
                                              "usuario" : resultado_login["usuario"] ,
                                              "lista_fichajes" : get_fichajes_service(sesion , None)
                                          })
