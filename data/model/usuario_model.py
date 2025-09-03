from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    idUsuario: int
    nome: str
    cpf: str
    email: str
    senha: str
    genero: str
    dataNascimento: str
    perfil: str = 'paciente'
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None
