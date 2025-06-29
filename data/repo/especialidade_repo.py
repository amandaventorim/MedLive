from typing import Optional
from data.model.especialidade_model import Especialidade
from data.sql.especialidade_sql import *
from data.util import get_connection


def criar_tabela_especialidade() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_ESPECIALIDADE)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela especialidade: {e}")
        return False


def inserir_especialidade(especialidade: Especialidade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_ESPECIALIDADE, (
            especialidade.nome,
            especialidade.descricao
        ))
        return cursor.lastrowid


def obter_todas_especialidades() -> list[Especialidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_ESPECIALIDADES)
        rows = cursor.fetchall()
        especialidades = [
            Especialidade(
                idEspecialidade=row["idEspecialidade"],
                nome=row["nome"],
                descricao=row["descricao"]
            ) for row in rows
        ]
        return especialidades

def obter_especialidades_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Especialidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_ESPECIALIDADES_POR_PAGINA, (tamanho_pagina, offset))
        rows = cursor.fetchall()
        especialidades = [
            Especialidade(
                idEspecialidade=row["idEspecialidade"],
                nome=row["nome"],
                descricao=row["descricao"]
            ) for row in rows
        ]
        return especialidades

def obter_especialidade_por_id(idEspecialidade: int) -> Optional[Especialidade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ESPECIALIDADE_POR_ID, (idEspecialidade,))
        row = cursor.fetchone()
        if row:
            return Especialidade(
                idEspecialidade=row["idEspecialidade"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None


def atualizar_especialidade(especialidade: Especialidade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_ESPECIALIDADE, (
            especialidade.nome,
            especialidade.descricao,
            especialidade.idEspecialidade
        ))
        return cursor.rowcount > 0


def deletar_especialidade(idEspecialidade: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ESPECIALIDADE, (idEspecialidade,))
        return cursor.rowcount > 0
