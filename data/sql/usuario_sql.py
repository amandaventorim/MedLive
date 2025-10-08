CRIAR_TABELA_USUARIO = """
CREATE TABLE IF NOT EXISTS usuario (
idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
cpf TEXT NOT NULL,
email TEXT NOT NULL,
senha TEXT NOT NULL,
genero TEXT NOT NULL,
dataNascimento TEXT NOT NULL,
perfil TEXT NOT NULL DEFAULT 'paciente',
foto TEXT,
token_redefinicao TEXT,
data_token TIMESTAMP,
data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR_USUARIO = """
INSERT INTO usuario (nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS_USUARIOS = """
SELECT 
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
ORDER BY idUsuario
"""

OBTER_USUARIOS_POR_PAGINA = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
ORDER BY idUsuario
LIMIT ? OFFSET ?
"""

OBTER_USUARIO_POR_ID = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE idUsuario = ?
"""
# SQL para obter usuário por email
OBTER_USUARIO_POR_EMAIL = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE email = ?
"""

# SQL para obter usuário por CPF
OBTER_USUARIO_POR_CPF = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE cpf = ?
"""

# SQL para obter usuário por senha
OBTER_USUARIO_POR_SENHA = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE senha = ?
"""

OBTER_TODOS_USUARIOS_POR_PERFIL = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento, perfil, foto, token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE perfil = ?
"""

UPDATE_USUARIO = """
UPDATE usuario
SET nome = ?, cpf = ?, email = ?, genero = ?, dataNascimento = ?, perfil = ?, foto = ?, token_redefinicao = ?, data_token = ?, data_cadastro = ?
WHERE idUsuario = ?
"""

UPDATE_SENHA_USUARIO = """
UPDATE usuario
SET senha = ?
WHERE idUsuario = ?
"""

# Atualizar apenas a foto do usuário
UPDATE_FOTO_USUARIO = """
UPDATE usuario SET foto = ? WHERE idUsuario = ?
"""

DELETAR_USUARIO = """
DELETE FROM usuario
WHERE idUsuario = ?
"""