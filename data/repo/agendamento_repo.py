from typing import Optional
from data.model.agendamento_model import Agendamento
from data.sql.agendamento_sql import *
from data.util import get_connection


def criar_tabela_agendamento() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_AGENDAMENTO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela agendamento: {e}")
        return False


def inserir_agendamento(agendamento: Agendamento) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_AGENDAMENTO, (
            agendamento.idPaciente,
            agendamento.idMedico,
            agendamento.dataAgendamento,
            agendamento.horario,
            agendamento.status,
            agendamento.queixa,
            agendamento.preco
        ))
        return cursor.lastrowid


def obter_todos_agendamentos() -> list[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_AGENDAMENTOS)
        rows = cursor.fetchall()
        return [
            Agendamento(
                idAgendamento=row["idAgendamento"],
                idPaciente=row["idPaciente"],
                idMedico=row["idMedico"],
                dataAgendamento=row["dataAgendamento"],
                horario=row["horario"],
                status=row["status"],
                queixa=row["queixa"],
                preco=row["preco"],
                dataInclusao=row["dataInclusao"]
            )
            for row in rows
        ]

def obter_agendamentos_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_AGENDAMENTOS_POR_PAGINA, (tamanho_pagina, offset))
        rows = cursor.fetchall()
        return [
            Agendamento(
                idAgendamento=row["idAgendamento"],
                idPaciente=row["idPaciente"],
                idMedico=row["idMedico"],
                dataAgendamento=row["dataAgendamento"],
                horario=row["horario"],
                status=row["status"],
                queixa=row["queixa"],
                preco=row["preco"],
                dataInclusao=row["dataInclusao"]
            )
            for row in rows
        ]

def obter_agendamento_por_id(idAgendamento: int) -> Optional[Agendamento]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_AGENDAMENTO_POR_ID, (idAgendamento,))
        row = cursor.fetchone()
        if row:
            return Agendamento(
                idAgendamento=row["idAgendamento"],
                idPaciente=row["idPaciente"],
                idMedico=row["idMedico"],
                dataAgendamento=row["dataAgendamento"],
                horario=row["horario"],
                status=row["status"],
                queixa=row["queixa"],
                preco=row["preco"],
                dataInclusao=row["dataInclusao"]
            )
        return None


def atualizar_agendamento(agendamento: Agendamento) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_AGENDAMENTO, (
            agendamento.idPaciente,
            agendamento.idMedico,
            agendamento.dataAgendamento,
            agendamento.horario,
            agendamento.status,
            agendamento.queixa,
            agendamento.preco,
            agendamento.idAgendamento
        ))
        return cursor.rowcount > 0


def deletar_agendamento(idAgendamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_AGENDAMENTO, (idAgendamento,))
        return cursor.rowcount > 0
