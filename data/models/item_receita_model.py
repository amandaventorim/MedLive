from dataclasses import dataclass


@dataclass
class ItemReceita:
    idConsulta: int
    idMedicamento: int
    descricao: str