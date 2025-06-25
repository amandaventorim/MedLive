from typing import Optional
from data.model.administrador_model import Administrador
from data.sql.administrador_sql import *
from data.sql.usuario_sql import *
from data.util import get_connection


def criar_tabela_administrador() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_ADMINISTRADOR)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela administrador: {e}")
        return False


def inserir_administrador(administrador: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            administrador.nome,
            administrador.cpf,
            administrador.email,
            administrador.senha,
            administrador.genero,
            administrador.dataNascimento))
        
        id_administrador = cursor.lastrowid  

        cursor.execute(INSERIR_ADMINISTRADOR, (
            id_administrador,))
        return id_administrador


def obter_todos_administradores() -> list[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_ADMINISTRADORES)
        rows = cursor.fetchall()
        administradores = [
            Administrador(
                idAdministrador=row["idAdministrador"],
                idUsuario=row["idAdministrador"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"])
            for row in rows]
        return administradores


def obter_administrador_por_id(idAdministrador: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ADMINISTRADOR_POR_ID, (idAdministrador,))
        row = cursor.fetchone()
        if row:
            return Administrador(
                idAdministrador=row["idAdministrador"],
                idUsuario=row["idAdministrador"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],  
                genero=row["genero"],
                dataNascimento=row["dataNascimento"]
            )
        return None
    

def atualizar_administrador(administrador: Administrador) -> bool:
    if obter_administrador_por_id(administrador.idAdministrador):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_USUARIO, (
                administrador.nome,
                administrador.cpf,
                administrador.email,
                administrador.genero,
                administrador.dataNascimento,
                administrador.idUsuario
            ))
            return cursor.rowcount > 0
    return False
      

def atualizar_senha_administrador(idAdministrador: int, senha: str) -> bool:
    if obter_administrador_por_id(idAdministrador):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_SENHA_USUARIO, (senha, idAdministrador))
            return cursor.rowcount > 0
    return False


def deletar_administrador(idAdministrador: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ADMINISTRADOR, (idAdministrador,))
        if cursor.rowcount > 0:
            cursor.execute(DELETAR_USUARIO, (idAdministrador,))
        return cursor.rowcount > 0
