from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import secrets


app = FastAPI()

# Gerar chave secreta (em produção, use variável de ambiente!)
SECRET_KEY = secrets.token_urlsafe(32)

# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=28800,  # Sessão expira em 8 horas
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)


router = APIRouter()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)

from routes import public
app.include_router(public.router)

from routes import auth_routes
app.include_router(auth_routes.router)

from routes import perfil_routes
app.include_router(perfil_routes.router)

from routes.paciente import paciente_rotas, cadastro_paciente, consulta_rotas
app.include_router(paciente_rotas.router)
app.include_router(cadastro_paciente.router)
app.include_router(consulta_rotas.router)
from routes.medico import medico_rotas, cadastro_medico
app.include_router(medico_rotas.router)
app.include_router(cadastro_medico.router)

from routes.admin import admin_rotas
app.include_router(admin_rotas.router)

