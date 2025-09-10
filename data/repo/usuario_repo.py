from typing import Optional
from data.model.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import get_connection

def criar_tabela_usuario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_USUARIO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela usuario: {e}")
        return False


def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            usuario.nome,
            usuario.cpf,
            usuario.email,
            usuario.senha,
            usuario.genero,
            usuario.dataNascimento,
            usuario.perfil,
            usuario.foto,
            usuario.token_redefinicao,
            usuario.data_token,
            usuario.data_cadastro))
        return cursor.lastrowid

def obter_todos_usuarios() -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_USUARIOS)
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                idUsuario=row["idUsuario"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"])
            for row in rows]
        return usuarios
    
def obter_usuarios_por_pagina(numero_pagina: int, tamanho_pagina: int) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        limit = tamanho_pagina
        offset = (numero_pagina - 1) * tamanho_pagina
        cursor.execute(OBTER_USUARIOS_POR_PAGINA, (limit, offset))
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                idUsuario=row["idUsuario"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"])
            for row in rows]
        return usuarios
    
    
def obter_usuario_por_id(idUsuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_ID, (idUsuario,))
        row = cursor.fetchone()
        if row:
            usuario = Usuario(
                idUsuario=row["idUsuario"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"])
            return usuario

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                idUsuario=row["idUsuario"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"]
            )
        return None
    
def atualizar_usuario(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_USUARIO, (
            usuario.nome,
            usuario.cpf,
            usuario.email,
            usuario.genero,
            usuario.dataNascimento,
            usuario.perfil,
            usuario.foto,
            usuario.token_redefinicao,
            usuario.data_token,
            usuario.data_cadastro,
            usuario.idUsuario))
        return cursor.rowcount > 0
    
def atualizar_senha_usuario(idUsuario: int, nova_senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_SENHA_USUARIO, (nova_senha, idUsuario))
        return cursor.rowcount > 0
    
def deletar_usuario(idUsuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_USUARIO, (idUsuario,))
        return cursor.rowcount > 0

def obter_todos_usuarios_por_perfil(perfil: str) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_USUARIOS_POR_PERFIL, (perfil,))
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                idUsuario=row["idUsuario"],
                nome=row["nome"],
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"],
                perfil=row["perfil"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                data_cadastro=row["data_cadastro"])
            for row in rows if row["perfil"] == perfil]
        return usuarios

