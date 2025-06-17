from typing import Optional
from usuario_model import Usuario
from usuario_sql import *
from util import get_connection

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
    

criar_tabela_usuario()
# inserir_usuario(Usuario(
#     idUsuario = 0,
#     nome="fernando Silva",
#     cpf="12345678901",
#     email="silva@gmail.com",
#     senha="123", 
#     genero="feminino",
#     dataNascimento="1990-01-01"))

# obter_todos_usuarios()
# for usuario in obter_todos_usuarios():
#     print(usuario)

# print(obter_usuario_por_id(1))

# print(atualizar_usuario(Usuario( nome="eros", 
#     cpf="12345678901",
#     email="eros@fmail",
#     senha="123",
#     genero="masculino",
#     dataNascimento="1990-01-01",
#     idUsuario=1)))

# print(deletar_usuario(1))