from dataclasses import dataclass
from data.model.usuario_model import Usuario


@dataclass
class Administrador(Usuario):
    idAdministrador: int