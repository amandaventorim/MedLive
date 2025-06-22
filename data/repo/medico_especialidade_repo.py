from typing import Optional
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.sql.medico_especialidade_sql import *
from data.util import get_connection

from typing import Optional
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.sql.medico_especialidade_sql import *
from data.util import get_connection


def criar_tabela_medico_especialidade() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_MEDICO_ESPECIALIDADE)
        return cursor.rowcount >= 0


def inserir_medico_especialidade(medico_especialidade: MedicoEspecialidade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_MEDICO_ESPECIALIDADE, (
            medico_especialidade.idMedico,
            medico_especialidade.idEspecialidade,
            medico_especialidade.dataHabilitacao))
        return cursor.rowcount
        


def obter_todos_medicos_especialidades() -> list[MedicoEspecialidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_MEDICOS_ESPECIALIDADES)
        rows = cursor.fetchall()
        return [
            MedicoEspecialidade(
                idMedico=row["idMedico"],
                idEspecialidade=row["idEspecialidade"],
                dataHabilitacao=row["dataHabilitacao"]) 
                for row in rows]


def obter_medico_especialidade_por_id(idMedico: int, idEspecialidade: int) -> Optional[MedicoEspecialidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MEDICO_ESPECIALIDADE_POR_ID, (idMedico, idEspecialidade))
        row = cursor.fetchone()
        if row:
            return MedicoEspecialidade(
                idMedico=row["idMedico"],
                idEspecialidade=row["idEspecialidade"],
                dataHabilitacao=row["dataHabilitacao"])
        return None


def atualizar_medico_especialidade(medico_especialidade: MedicoEspecialidade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_MEDICO_ESPECIALIDADE, (
            medico_especialidade.dataHabilitacao,
            medico_especialidade.idMedico,
            medico_especialidade.idEspecialidade
        ))
        return cursor.rowcount > 0


def deletar_medico_especialidade(idMedico: int, idEspecialidade: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MEDICO_ESPECIALIDADE, (idMedico, idEspecialidade))
        return cursor.rowcount > 0
