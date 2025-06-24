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

OBTER_USUARIO_POR_ID = """
SELECT
idUsuario, nome, cpf, email, senha, genero, dataNascimento
FROM usuario
WHERE idUsuario = ?
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