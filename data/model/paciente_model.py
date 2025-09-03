from dataclasses import dataclass
from typing import Optional
from data.model.usuario_model import Usuario

@dataclass
class Paciente(Usuario):
    idPaciente: Optional[int] = None
    endereco: str = ""
    convenio: str = ""
    