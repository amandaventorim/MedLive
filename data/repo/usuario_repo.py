from typing import Optional
from data.model.usuario_model import Usuario
from data.sql.usuario_sql import *
from data.util import get_connection

def criar_tabela_usuario() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_USUARIO)
        return cursor.rowcount > 0

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            usuario.nome, 
            usuario.cpf, 
            usuario.email, 
            usuario.senha, 
            usuario.genero,
            usuario.dataNascimento))
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
                dataNascimento=row["dataNascimento"]) 
                for row in rows]
        return usuarios
    
    
def obter_usuario_por_id(idUsuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_ID, (idUsuario,))
        row = cursor.fetchone()
        usuario = Usuario(
                idUsuario=row["idUsuario"], 
                nome=row["nome"], 
                cpf=row["cpf"],
                email=row["email"],
                senha=row["senha"],
                genero=row["genero"],
                dataNascimento=row["dataNascimento"])
        return usuario if row else None
    
def atualizar_usuario(usuario: Usuario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(UPDATE_USUARIO, (
            usuario.nome, 
            usuario.cpf, 
            usuario.email, 
            usuario.senha, 
            usuario.genero,
            usuario.dataNascimento,
            usuario.idUsuario))
        return cursor.rowcount > 0
    
def deletar_usuario(idUsuario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_USUARIO, (idUsuario,))
        return cursor.rowcount > 0
    


