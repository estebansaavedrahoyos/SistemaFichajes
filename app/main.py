from app.services.general_service import crear_db , crear_primer_motivo
from fastapi import FastAPI 
from app.routers.puesto_router import router as puestos_router
from app.routers.motivo_router import router as motivos_router
from app.routers.empleado_router import router as empleados_router 
from app.routers.fichaje_router import router as fichajes_router
from app.routers.web_router import router as web_router


app = FastAPI(title="Sistema de Fichajes") 

crear_db()
crear_primer_motivo()

usuario_activo = None 



app.include_router(puestos_router) 
app.include_router(motivos_router) 
app.include_router(empleados_router)
app.include_router(fichajes_router)
app.include_router(web_router)