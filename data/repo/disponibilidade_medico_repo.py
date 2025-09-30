from typing import Optional, List
from data.model.disponibilidade_medico_model import DisponibilidadeMedico
from data.sql.disponibilidade_medico_sql import *
from data.util import get_connection


def criar_tabela_disponibilidade_medico() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_DISPONIBILIDADE_MEDICO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela disponibilidade_medico: {e}")
        return False


def inserir_disponibilidade_medico(disponibilidade: DisponibilidadeMedico) -> Optional[int]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERIR_DISPONIBILIDADE_MEDICO, (
                disponibilidade.idMedico,
                disponibilidade.diaSemana,
                disponibilidade.horaInicio,
                disponibilidade.horaFim,
                disponibilidade.ativo
            ))
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir disponibilidade do médico: {e}")
        return None


def obter_disponibilidades_por_medico(idMedico: int) -> List[DisponibilidadeMedico]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_DISPONIBILIDADES_POR_MEDICO, (idMedico,))
            rows = cursor.fetchall()
            return [
                DisponibilidadeMedico(
                    idDisponibilidade=row["idDisponibilidade"],
                    idMedico=row["idMedico"],
                    diaSemana=row["diaSemana"],
                    horaInicio=row["horaInicio"],
                    horaFim=row["horaFim"],
                    ativo=bool(row["ativo"]),
                    dataInclusao=row["dataInclusao"]
                ) for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter disponibilidades do médico: {e}")
        return []


def obter_disponibilidade_por_id(idDisponibilidade: int) -> Optional[DisponibilidadeMedico]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_DISPONIBILIDADE_POR_ID, (idDisponibilidade,))
            row = cursor.fetchone()
            if row:
                return DisponibilidadeMedico(
                    idDisponibilidade=row["idDisponibilidade"],
                    idMedico=row["idMedico"],
                    diaSemana=row["diaSemana"],
                    horaInicio=row["horaInicio"],
                    horaFim=row["horaFim"],
                    ativo=bool(row["ativo"]),
                    dataInclusao=row["dataInclusao"]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter disponibilidade por ID: {e}")
        return None


def atualizar_disponibilidade_medico(disponibilidade: DisponibilidadeMedico) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(ATUALIZAR_DISPONIBILIDADE_MEDICO, (
                disponibilidade.diaSemana,
                disponibilidade.horaInicio,
                disponibilidade.horaFim,
                disponibilidade.ativo,
                disponibilidade.idDisponibilidade
            ))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar disponibilidade do médico: {e}")
        return False


def deletar_disponibilidade_medico(idDisponibilidade: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR_DISPONIBILIDADE_MEDICO, (idDisponibilidade,))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar disponibilidade do médico: {e}")
        return False


def deletar_todas_disponibilidades_medico(idMedico: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETAR_TODAS_DISPONIBILIDADES_MEDICO, (idMedico,))
            return cursor.rowcount >= 0  # Pode deletar 0 ou mais registros
    except Exception as e:
        print(f"Erro ao deletar todas disponibilidades do médico: {e}")
        return False
