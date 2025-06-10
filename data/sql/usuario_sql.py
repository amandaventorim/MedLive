CRIAR_TABELA = """
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

INSERIR = """
INSERT INTO cliente (nome, cpf, email, telefone, senha) 
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODOS = """
SELECT 
id, nome, cpf, email, telefone, senha
FROM cliente
ORDER BY nome
""" 