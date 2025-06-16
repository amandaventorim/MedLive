from dataclasses import dataclass


@dataclass
class Consulta:
    idConsulta: int
    dataHora: str
    queixa: str
    conduta: str
    idMedico: int
    idPaciente: int