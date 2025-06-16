from dataclasses import dataclass


@dataclass
class EntradaProntuario:
    idProntuario: int
    data: str
    queixaPrincipal: str
    alergias: str
    solicitacoesExames: str
    antecedentesFamiliares: str
    fatoresAlivio: str
    fatoresPiora: str
    fatoresPredecessores: str
    idConsulta: int