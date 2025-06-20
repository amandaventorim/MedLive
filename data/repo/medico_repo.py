from typing import Optional
from data.model.medico_model import Medico
from data.repo.usuario_repo import inserir_usuario
from data.sql.medico_sql import *
from data.sql.usuario_sql import *
from data.util import get_connection


def criar_tabela_medico() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_MEDICO)
        return cursor.rowcount > 0


# INSERIR APENAS MEDICO (presume que o usuário já existe)
def inserir_medico(medico: Medico) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_MEDICO, (
            medico.idMedico,
            medico.crm,
            medico.statusProfissional
        ))
        return cursor.lastrowid


# INSERIR USUARIO PRIMEIRO E DEPOIS MEDICO (tudo junto)
def inserir_usuario_medico(medico: Medico) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            medico.nome,
            medico.cpf,
            medico.email,
            medico.senha,
            medico.genero,
            medico.dataNascimento
        ))
        id_medico = cursor.lastrowid  # idMedico = idUsuario

        cursor.execute(INSERIR_MEDICO, (
            id_medico,
            medico.crm,
            medico.statusProfissional
        ))
        return id_medico


def obter_todos_medicos() -> list[Medico]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_MEDICOS)
        rows = cursor.fetchall()
        medicos = [
            Medico(
                idMedico=row["idMedico"],
                idUsuario=row["idMedico"],  # mesmo valor
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                crm=row["crm"],
                statusProfissional=row["statusProfissional"])
            for row in rows
        ]
        return medicos


def obter_medico_por_id(idMedico: int) -> Optional[Medico]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MEDICOS_POR_ID, (idMedico,))
        row = cursor.fetchone()
        if row:
            return Medico(
                idMedico=row["idMedico"],
                idUsuario=row["idMedico"],  # mesmo valor
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                crm=row["crm"],
                statusProfissional=row["statusProfissional"]
            )
        return None


def atualizar_medico(medico: Medico) -> bool:  #fazer update de usuario também?
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_MEDICO, (
            medico.crm,
            medico.statusProfissional,
            medico.idMedico
        ))
        return cursor.rowcount > 0


def deletar_medico(idMedico: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MEDICO, (idMedico,))
        return cursor.rowcount > 0


def deletar_usuario_medico(idMedico: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MEDICO, (idMedico,))
        if cursor.rowcount > 0:
            cursor.execute(DELETAR_USUARIO, (idMedico,))
        return cursor.rowcount > 0
