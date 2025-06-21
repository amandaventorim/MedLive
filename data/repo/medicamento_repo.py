from typing import Optional
from data.model.medicamento_model import Medicamento
from data.sql.medicamento_sql import *
from data.util import get_connection


def criar_tabela_medicamento() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_MEDICAMENTO)
        return cursor.rowcount > 0


def inserir_medicamento(medicamento: Medicamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_MEDICAMENTO, (
            medicamento.nome,
        ))
        return cursor.lastrowid


def obter_todos_medicamentos() -> list[Medicamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_MEDICAMENTOS)
        rows = cursor.fetchall()
        medicamentos = [
            Medicamento(
                idMedicamento=row["idMedicamento"],
                nome=row["nome"]
            ) for row in rows
        ]
        return medicamentos


def obter_medicamento_por_id(idMedicamento: int) -> Optional[Medicamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MEDICAMENTO_POR_ID, (idMedicamento,))
        row = cursor.fetchone()
        if row:
            return Medicamento(
                idMedicamento=row["idMedicamento"],
                nome=row["nome"]
            )
        return None


def atualizar_medicamento(medicamento: Medicamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_MEDICAMENTO, (
            medicamento.nome,
            medicamento.idMedicamento
        ))
        return cursor.rowcount > 0


def deletar_medicamento(idMedicamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MEDICAMENTO, (idMedicamento,))
        return cursor.rowcount > 0
