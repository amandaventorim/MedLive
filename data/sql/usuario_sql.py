CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS usuario (
idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
cpf TEXT NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL,
genero TEXT NOT NULL,
dataNascimento TEXT NOT NULL
);
"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, cpf, email, senha, genero, dataNascimento) 
VALUES (?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS_USUARIOS = """
SELECT 
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
ORDER BY idUsuario
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
ORDER BY idUsuario
LIMIT ? OFFSET ?
"""

OBTER_USUARIO_POR_ID = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
WHERE idUsuario = ?
"""
# SQL para obter usuário por email
OBTER_USUARIO_POR_EMAIL = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
WHERE email = ?
"""

# SQL para obter usuário por senha
OBTER_USUARIO_POR_SENHA = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
WHERE senha = ?
"""

UPDATE_USUARIO = """
UPDATE usuario
SET nome = ?, cpf = ?, email = ?, genero = ?, dataNascimento = ?
WHERE idUsuario = ?
"""

UPDATE_SENHA_USUARIO = """
UPDATE usuario
SET senha = ?
WHERE idUsuario = ?
"""

DELETAR_USUARIO = """
DELETE FROM usuario
WHERE idUsuario = ?
"""