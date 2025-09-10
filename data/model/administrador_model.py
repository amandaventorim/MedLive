from dataclasses import dataclass, field
from typing import Optional
from data.model.usuario_model import Usuario

@dataclass
class Administrador(Usuario):
    idAdministrador: Optional[int] = field(default=None)