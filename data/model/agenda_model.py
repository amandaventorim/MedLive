from dataclasses import dataclass


@dataclass
class Agenda:
    idAgenda: int
    idMedico: int
    dataHora: str
    disponivel: bool