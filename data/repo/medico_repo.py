from typing import Optional
from data.model.medico_model import Medico
from data.sql.medico_sql import *
from data.sql.usuario_sql import *
from data.util import get_connection


def criar_tabela_medico() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_MEDICO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela medico: {e}")
        return False


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
        id_medico = cursor.lastrowid  

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
                idUsuario=row["idMedico"],  
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
                idUsuario=row["idMedico"], 
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


def atualizar_medico(medico: Medico) -> bool:
    if obter_medico_por_id(medico.idMedico):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_USUARIO, (
                medico.nome,
                medico.cpf,
                medico.email,
                medico.genero,
                medico.dataNascimento,
                medico.idUsuario
            ))
            if cursor.rowcount > 0:
                cursor.execute(UPDATE_MEDICO, (
                    medico.crm,
                    medico.statusProfissional,
                    medico.idMedico
                ))
            return cursor.rowcount > 0
    return False


def atualizar_senha_medico(idMedico: int, senha: str) -> bool:
    if obter_medico_por_id(idMedico):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_SENHA_USUARIO, (senha, idMedico))
            return cursor.rowcount > 0
    return False


def deletar_usuario_medico(idMedico: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MEDICO, (idMedico,))
        if cursor.rowcount > 0:
            cursor.execute(DELETAR_USUARIO, (idMedico,))
        return cursor.rowcount > 0
