CRIAR_TABELA_MEDICAMENTO = """
CREATE TABLE IF NOT EXISTS medicamento (
idMedicamento INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL
);
"""

INSERIR_MEDICAMENTO = """
INSERT INTO medicamento (nome)
VALUES (?)
"""

OBTER_TODOS_MEDICAMENTOS = """
SELECT * FROM medicamento
"""

OBTER_MEDICAMENTO_POR_ID = """
SELECT * FROM medicamento
WHERE idMedicamento = ?
"""

UPDATE_MEDICAMENTO = """
UPDATE medicamento
SET nome = ?
WHERE idMedicamento = ?
"""

DELETAR_MEDICAMENTO = """
DELETE FROM medicamento
WHERE idMedicamento = ?
"""
