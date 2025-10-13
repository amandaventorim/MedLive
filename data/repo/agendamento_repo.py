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
    try:
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
    except Exception as e:
        print(f"Erro ao inserir agendamento: {e}")
        return None


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


def obter_agendamentos_por_paciente(idPaciente: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_AGENDAMENTOS_POR_PACIENTE, (idPaciente,))
        rows = cursor.fetchall()
        return [
            {
                "idAgendamento": row["idAgendamento"],
                "idPaciente": row["idPaciente"],
                "idMedico": row["idMedico"],
                "dataAgendamento": row["dataAgendamento"],
                "horario": row["horario"],
                "status": row["status"],
                "queixa": row["queixa"],
                "preco": row["preco"],
                "dataInclusao": row["dataInclusao"],
                "nomeMedico": row["nomeMedico"],
                "crm": row["crm"],
                "fotoMedico": row["fotoMedico"]
            }
            for row in rows
        ]


def obter_agendamentos_por_medico(idMedico: int) -> list[dict]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_AGENDAMENTOS_POR_MEDICO, (idMedico,))
            rows = cursor.fetchall()
            
            if not rows:
                return []
                
            return [
                {
                    "idAgendamento": row["idAgendamento"],
                    "idPaciente": row["idPaciente"],
                    "idMedico": row["idMedico"],
                    "dataAgendamento": row["dataAgendamento"],
                    "horario": row["horario"],
                    "status": row["status"],
                    "queixa": row["queixa"] if row["queixa"] else "",
                    "preco": row["preco"] if row["preco"] else 0.0,
                    "dataInclusao": row["dataInclusao"],
                    "nomePaciente": row["nomePaciente"],
                    "endereco": row["endereco"] if row["endereco"] else "",
                    "convenio": row["convenio"] if row["convenio"] else "",
                    "emailPaciente": row["emailPaciente"] if row["emailPaciente"] else ""
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter agendamentos por médico {idMedico}: {e}")
        return []


def obter_agendamentos_por_medico_simples(idMedico: int) -> list[dict]:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_AGENDAMENTOS_POR_MEDICO_SIMPLES, (idMedico,))
            rows = cursor.fetchall()
            
            if not rows:
                return []
                
            return [
                {
                    "idAgendamento": row["idAgendamento"],
                    "idPaciente": row["idPaciente"],
                    "idMedico": row["idMedico"],
                    "dataAgendamento": row["dataAgendamento"],
                    "horario": row["horario"],
                    "status": row["status"],
                    "queixa": row["queixa"] if row["queixa"] else "",
                    "preco": row["preco"] if row["preco"] else 0.0,
                    "dataInclusao": row["dataInclusao"],
                    "nomePaciente": "Paciente",  # Placeholder
                    "endereco": "",  # Placeholder
                    "convenio": "",  # Placeholder
                    "emailPaciente": ""  # Placeholder
                }
                for row in rows
            ]
    except Exception as e:
        print(f"Erro ao obter agendamentos simples por médico {idMedico}: {e}")
        return []


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


def atualizar_status_agendamento(idAgendamento: int, novo_status: str, room_id: str = None) -> bool:
    """Atualiza o status de um agendamento e opcionalmente adiciona room_id"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Se temos room_id, vamos precisar de uma coluna para armazená-lo
            # Por ora, vamos apenas atualizar o status
            cursor.execute("UPDATE Agendamento SET status = ? WHERE idAgendamento = ?", 
                         (novo_status, idAgendamento))
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar status do agendamento: {e}")
        return False
