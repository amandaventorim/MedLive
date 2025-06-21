from typing import Optional
from data.model.entrada_prontuario_model import EntradaProntuario
from data.sql.entrada_prontuario_sql import *
from data.util import get_connection


def criar_tabela_entrada_prontuario() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_ENTRADA_PRONTUARIO)
        return cursor.rowcount >= 0


def inserir_entrada_prontuario(entrada: EntradaProntuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_ENTRADA_PRONTUARIO, (
            entrada.idConsulta,
            entrada.data,
            entrada.queixaPrincipal,
            entrada.alergias,
            entrada.solicitacoesExames,
            entrada.antecedentesFamiliares,
            entrada.fatoresAlivio,
            entrada.fatoresPiora,
            entrada.fatoresPredecessores
        ))
        return cursor.lastrowid


def obter_todas_entradas_prontuario() -> list[EntradaProntuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_ENTRADAS_PRONTUARIO)
        rows = cursor.fetchall()
        entradas = [
            EntradaProntuario(
                idProntuario=row["idProntuario"],
                idConsulta=row["idConsulta"],
                data=row["data"],
                queixaPrincipal=row["queixaPrinicipal"],
                alergias=row["alergias"],
                solicitacoesExames=row["solicitacoesExames"],
                antecedentesFamiliares=row["antecedoresFamiliares"],
                fatoresAlivio=row["fatoresAlivio"],
                fatoresPiora=row["fatoresPiora"],
                fatoresPredecessores=row["fatoresPredecessores"]
            ) for row in rows
        ]
        return entradas


def obter_entrada_prontuario_por_id(idProntuario: int) -> Optional[EntradaProntuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ENTRADA_PRONTUARIO_POR_ID, (idProntuario,))
        row = cursor.fetchone()
        if row:
            return EntradaProntuario(
                idProntuario=row["idProntuario"],
                idConsulta=row["idConsulta"],
                data=row["data"],
                queixaPrincipal=row["queixaPrinicipal"],
                alergias=row["alergias"],
                solicitacoesExames=row["solicitacoesExames"],
                antecedentesFamiliares=row["antecedoresFamiliares"],
                fatoresAlivio=row["fatoresAlivio"],
                fatoresPiora=row["fatoresPiora"],
                fatoresPredecessores=row["fatoresPredecessores"]
            )
        return None


def atualizar_entrada_prontuario(entrada: EntradaProntuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_ENTRADA_PRONTUARIO, (
            entrada.idConsulta,
            entrada.data,
            entrada.queixaPrincipal,
            entrada.alergias,
            entrada.solicitacoesExames,
            entrada.antecedentesFamiliares,
            entrada.fatoresAlivio,
            entrada.fatoresPiora,
            entrada.fatoresPredecessores,
            entrada.idProntuario
        ))
        return cursor.rowcount > 0


def deletar_entrada_prontuario(idProntuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ENTRADA_PRONTUARIO, (idProntuario,))
        return cursor.rowcount > 0
