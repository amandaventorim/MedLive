from dataclasses import dataclass
from typing import Optional


@dataclass
class DisponibilidadeMedico:
    idDisponibilidade: int
    idMedico: int
    diaSemana: int  # 1 = Segunda, 2 = Terça, ..., 7 = Domingo
    horaInicio: str  # Formato HH:MM
    horaFim: str     # Formato HH:MM
    ativo: bool
    dataInclusao: Optional[str] = None
