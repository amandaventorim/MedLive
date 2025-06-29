from typing import Optional
from data.model.agenda_model import Agenda
from data.sql.agenda_sql import *
from data.util import get_connection


def criar_tabela_agenda() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_AGENDA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela agenda: {e}")
        return False


def inserir_agenda(agenda: Agenda) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_AGENDA, (
            agenda.idMedico,
            agenda.dataHora,
            agenda.disponivel))
        return cursor.lastrowid
       


def obter_todas_agendas() -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_AGENDAS)
        rows = cursor.fetchall()
        return [
            Agenda(
                idAgenda=row["idAgenda"],
                idMedico=row["idMedico"],
                dataHora=row["dataHora"],
                disponivel=bool(row["disponivel"])
            ) for row in rows
        ]

def obter_agendas_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_AGENDAS_POR_PAGINA, (tamanho_pagina, offset))
        rows = cursor.fetchall()
        return [
            Agenda(
                idAgenda=row["idAgenda"],
                idMedico=row["idMedico"],
                dataHora=row["dataHora"],
                disponivel=bool(row["disponivel"])
            ) for row in rows
        ]

def obter_agenda_por_id(idAgenda: int) -> Optional[Agenda]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_AGENDA_POR_ID, (idAgenda,))
        row = cursor.fetchone()
        if row:
            return Agenda(
                idAgenda=row["idAgenda"],
                idMedico=row["idMedico"],
                dataHora=row["dataHora"],
                disponivel=bool(row["disponivel"])
            )
        return None


def atualizar_agenda(agenda: Agenda) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_AGENDA, (
            agenda.idMedico,
            agenda.dataHora,
            agenda.disponivel,
            agenda.idAgenda
        ))
        return cursor.rowcount > 0


def deletar_agenda(idAgenda: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_AGENDA, (idAgenda,))
        return cursor.rowcount > 0
