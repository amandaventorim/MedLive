from dataclasses import dataclass


@dataclass
class Usuario:
    idUsuario: int
    nome: str
    cpf: str
    email: str
    senha: str
    genero: str
    dataNascimento: str
