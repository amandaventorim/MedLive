from typing import Optional
from data.model.consulta_model import Consulta
from data.sql.consulta_sql import *
from data.util import get_connection


def criar_tabela_consulta() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_CONSULTA)
        return cursor.rowcount >= 0


def inserir_consulta(consulta: Consulta) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_CONSULTA, (
            consulta.idMedico,
            consulta.idPaciente,
            consulta.dataHora,
            consulta.queixa,
            consulta.conduta
        ))
        return cursor.lastrowid


def obter_todas_consultas() -> list[Consulta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_CONSULTAS)
        rows = cursor.fetchall()
        consultas = [
            Consulta(
                idConsulta=row["idConsulta"],
                idMedico=row["idMedico"],
                idPaciente=row["idPaciente"],
                dataHora=row["dataHora"],
                queixa=row["queixa"],
                conduta=row["conduta"]
            ) for row in rows
        ]
        return consultas


def obter_consulta_por_id(idConsulta: int) -> Optional[Consulta]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_CONSULTA_POR_ID, (idConsulta,))
        row = cursor.fetchone()
        if row:
            return Consulta(
                idConsulta=row["idConsulta"],
                idMedico=row["idMedico"],
                idPaciente=row["idPaciente"],
                dataHora=row["dataHora"],
                queixa=row["queixa"],
                conduta=row["conduta"]
            )
        return None


def atualizar_consulta(consulta: Consulta) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_CONSULTA, (
            consulta.idMedico,
            consulta.idPaciente,
            consulta.dataHora,
            consulta.queixa,
            consulta.conduta,
            consulta.idConsulta
        ))
        return cursor.rowcount > 0


def deletar_consulta(idConsulta: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_CONSULTA, (idConsulta,))
        return cursor.rowcount > 0
