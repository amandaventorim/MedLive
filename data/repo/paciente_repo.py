from typing import Optional
from data.model.paciente_model import Paciente
from data.sql.paciente_sql import *
from data.sql.usuario_sql import *
from data.util import get_connection


def criar_tabela_paciente() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_PACIENTE)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela paciente: {e}")
        return False

    
def inserir_paciente(paciente: Paciente) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            paciente.nome,
            paciente.cpf,
            paciente.email,
            paciente.senha,
            paciente.genero,
            paciente.dataNascimento
            ))
        id_paciente = cursor.lastrowid 

        cursor.execute(INSERIR_PACIENTE, (
            id_paciente,  
            paciente.endereco,
            paciente.convenio
            ))
        return id_paciente

def obter_todos_pacientes() -> list[Paciente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PACIENTES)
        rows = cursor.fetchall()
        pacientes = [
            Paciente(
                idPaciente=row["idPaciente"],
                idUsuario=row["idPaciente"], 
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                endereco=row["endereco"],
                convenio=row["convenio"])
                for row in rows ]
        return pacientes

def obter_pacientes_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Paciente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        limit = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_PACIENTES_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        pacientes = [
            Paciente(
                idPaciente=row["idPaciente"],
                idUsuario=row["idPaciente"],  
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                endereco=row["endereco"],
                convenio=row["convenio"])
                for row in rows ]
        return pacientes

def obter_paciente_por_id(idPaciente: int) -> Optional[Paciente]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PACIENTE_POR_ID, (idPaciente,))
        row = cursor.fetchone()
        if row:
            return Paciente(
                idPaciente=row["idPaciente"],
                idUsuario=row["idPaciente"],  
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                endereco=row["endereco"],
                convenio=row["convenio"] )
        return None


def atualizar_paciente(paciente: Paciente) -> bool:
    if obter_paciente_por_id(paciente.idPaciente):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_USUARIO, (
                paciente.nome,
                paciente.cpf,
                paciente.email,
                paciente.genero,
                paciente.dataNascimento,
                paciente.idUsuario))
            if cursor.rowcount > 0:
                cursor.execute(UPDATE_PACIENTE, (
                    paciente.endereco,
                    paciente.convenio,
                    paciente.idPaciente))
            return cursor.rowcount > 0
    return False


def atualizar_senha_paciente(idPaciente: int, senha: str) -> bool:
    if obter_paciente_por_id(idPaciente):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_SENHA_USUARIO, (senha, idPaciente))
            return cursor.rowcount > 0
    return False


def deletar_paciente(idPaciente: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_PACIENTE, (idPaciente,))
        if cursor.rowcount > 0:
            cursor.execute(DELETAR_USUARIO, (idPaciente,))
        return cursor.rowcount > 0

