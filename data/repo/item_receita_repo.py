from typing import Optional
from data.model.item_receita_model import ItemReceita
from data.sql.item_receita_sql import *
from data.util import get_connection


def criar_tabela_item_receita() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_ITEM_RECEITA)
        return cursor.rowcount >= 0


def inserir_item_receita(item_receita: ItemReceita) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_ITEM_RECEITA, (
            item_receita.idConsulta,
            item_receita.idMedicamento,
            item_receita.descricao))
        return cursor.lastrowid
        

def obter_todos_itens_receita() -> list[ItemReceita]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_ITENS_RECEITA)
        rows = cursor.fetchall()
        return [
            ItemReceita(
                idConsulta=row["idConsulta"],
                idMedicamento=row["idMedicamento"],
                descricao=row["descricao"]
            ) for row in rows
        ]


def obter_item_receita_por_id(idConsulta: int, idMedicamento: int) -> Optional[ItemReceita]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ITEM_RECEITA_POR_ID, (idConsulta, idMedicamento))
        row = cursor.fetchone()
        if row:
            return ItemReceita(
                idConsulta=row["idConsulta"],
                idMedicamento=row["idMedicamento"],
                descricao=row["descricao"]
            )
        return None


def atualizar_item_receita(item_receita: ItemReceita) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_ITEM_RECEITA, (
            item_receita.descricao,
            item_receita.idConsulta,
            item_receita.idMedicamento
        ))
        return cursor.rowcount > 0


def deletar_item_receita(idConsulta: int, idMedicamento: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ITEM_RECEITA, (idConsulta, idMedicamento))
        return cursor.rowcount > 0
