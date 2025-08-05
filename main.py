from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *
from data.model.medico_model import Medico
from data.repo.medico_repo import *
from data.model.administrador_model import Administrador
from data.repo.administrador_repo import *
from data.model.especialidade_model import Especialidade
from data.repo.especialidade_repo import *
from data.model.medicamento_model import Medicamento
from data.repo.medicamento_repo import *
from data.model.consulta_model import Consulta
from data.repo.consulta_repo import *
from data.model.entrada_prontuario_model import EntradaProntuario
from data.repo.entrada_prontuario_repo import *
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.repo.medico_especialidade_repo import *
from data.model.item_receita_model import ItemReceita
from data.repo.item_receita_repo import *   
from data.model.agenda_model import Agenda
from data.repo.agenda_repo import *
from data.model.agendamento_model import Agendamento
from data.repo.agendamento_repo import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root():
    response = templates.TemplateResponse("index.html", {"request": {}})
    return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)



