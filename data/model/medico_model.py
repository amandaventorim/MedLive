from dataclasses import dataclass
from data.model.usuario_model import Usuario


@dataclass
class Medico(Usuario):
    idMedico: int
    crm: str
    statusProfissional: str
