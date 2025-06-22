from dataclasses import dataclass


@dataclass
class MedicoEspecialidade:
    idMedico: int
    idEspecialidade: int
    dataHabilitacao: str