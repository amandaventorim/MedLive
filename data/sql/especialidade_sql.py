CRIAR_TABELA_ESPECIALIDADE = """
CREATE TABLE IF NOT EXISTS especialidade (
idEspecialidade INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL,
descricao TEXT NOT NULL
);
"""

INSERIR_ESPECIALIDADE = """
INSERT INTO especialidade (nome, descricao)
VALUES (?, ?)
"""

OBTER_TODAS_ESPECIALIDADES = """
SELECT * FROM especialidade
"""

OBTER_ESPECIALIDADE_POR_ID = """
SELECT * FROM especialidade
WHERE idEspecialidade = ?
"""

UPDATE_ESPECIALIDADE = """
UPDATE especialidade
SET nome = ?, descricao = ?
WHERE idEspecialidade = ?
"""

DELETAR_ESPECIALIDADE = """
DELETE FROM especialidade
WHERE idEspecialidade = ?
"""
