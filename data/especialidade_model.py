from dataclasses import dataclass


@dataclass
class Especialidade:
    idEspecialidade: int
    nome: str
    descricao: str