from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


router = APIRouter()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

from routes import public
app.include_router(public.router)

from routes.paciente import paciente_rotas, cadastro_paciente
app.include_router(paciente_rotas.router)
app.include_router(cadastro_paciente.router)

from routes.medico import medico_rotas
app.include_router(medico_rotas.router)

from routes.admin import admin_rotas
app.include_router(admin_rotas.router)