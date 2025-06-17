CRIAR_TABELA_ENTRADA_PRONTUARIO = """
CREATE TABLE IF NOT EXISTS entrada_prontuario (
idProntuario INTEGER PRIMARY KEY AUTOINCREMENT,
idConsulta INTEGER NOT NULL,
data TEXT NOT NULL,
queixaPrinicipal TEXT NOT NULL,
alergias TEXT,
solicitacoesExames TEXT,
antecedoresFamiliares TEXT,
fatoresAlivio TEXT,
fatoresPiora TEXT,
fatoresPredecessores TEXT,
FOREIGN KEY (idConsulta) REFERENCES consulta(idConsulta)
);
"""

INSERIR_ENTRADA_PRONTUARIO = """
INSERT INTO entrada_prontuario (idConsulta, data, queixaPrinicipal, alergias, solicitacoesExames, antecedoresFamiliares, fatoresAlivio, fatoresPiora, fatoresPredecessores)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODAS_ENTRADAS_PRONTUARIO = """
SELECT
idProntuario, idConsulta, data, queixaPrinicipal, alergias, solicitacoesExames, antecedoresFamiliares, fatoresAlivio, fatoresPiora, fatoresPredecessores
FROM entrada_prontuario 
ORDER BY idProntuario
"""

OBTER_ENTRADA_PRONTUARIO_POR_ID = """
SELECT
idProntuario, idConsulta, data, queixaPrinicipal, alergias, solicitacoesExames, antecedoresFamiliares, fatoresAlivio, fatoresPiora, fatoresPredecessores
FROM entrada_prontuario
WHERE idProntuario = ?
"""

UPDATE_ENTRADA_PRONTUARIO = """
UPDATE entrada_prontuario
SET idConsulta = ?, data = ?, queixaPrinicipal = ?, alergias = ?, solicitacoesExames = ?, antecedoresFamiliares = ?, fatoresAlivio = ?, fatoresPiora = ?, fatoresPredecessores = ?
WHERE idProntuario = ?
"""

DELETAR_ENTRADA_PRONTUARIO = """
DELETE FROM entrada_prontuario  
WHERE idProntuario = ?
"""
