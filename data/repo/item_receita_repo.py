from typing import Optional
from data.model.item_receita_model import ItemReceita
from data.sql.item_receita_sql import *
from data.util import get_connection


def criar_tabela_item_receita() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_ITEM_RECEITA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela item_receita: {e}")
        return False


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

def obter_itens_receita_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[ItemReceita]:
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_ITENS_RECEITA_POR_PAGINA, (tamanho_pagina, offset))
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
