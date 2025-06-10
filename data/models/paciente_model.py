from dataclasses import dataclass
from data.models.usuario_model import Usuario


@dataclass
class Paciente(Usuario):
    idPaciente: int
    endereco: str
    convenio: str
    telefone: str