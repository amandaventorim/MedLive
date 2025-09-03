from dataclasses import dataclass
from typing import Optional
from data.model.usuario_model import Usuario

@dataclass
class Medico(Usuario):
    idMedico: Optional[int] = None
    crm: str = ""
    statusProfissional: str = ""
