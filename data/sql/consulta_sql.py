CRIAR_TABELA_CONSULTA = """
CREATE TABLE IF NOT EXISTS consulta (
    idConsulta INTEGER PRIMARY KEY AUTOINCREMENT,
    idMedico INTEGER NOT NULL,
    idPaciente INTEGER NOT NULL,
    dataHora TEXT NOT NULL,
    queixa TEXT,
    conduta TEXT,
    FOREIGN KEY (idMedico) REFERENCES medico(idMedico),
    FOREIGN KEY (idPaciente) REFERENCES paciente(idPaciente)
);
"""

INSERIR_CONSULTA = """
INSERT INTO consulta (idMedico, idPaciente, dataHora, queixa, conduta)
VALUES (?, ?, ?, ?, ?)
"""

OBTER_TODAS_CONSULTAS = """
SELECT
c.idConsulta, c.dataHora, c.queixa, c.conduta, m.idMedico, p.idPaciente
FROM consulta c
JOIN medico m ON c.idMedico = m.idMedico
JOIN paciente p ON c.idPaciente = p.idPaciente
ORDER BY c.idConsulta;
"""

OBTER_CONSULTA_POR_ID = """
SELECT
c.idConsulta, c.dataHora, c.queixa, c.conduta, m.idMedico, p.idPaciente
FROM consulta c
JOIN medico m ON c.idMedico = m.idMedico
JOIN paciente p ON c.idPaciente = p.idPaciente
WHERE c.idConsulta = ?;
"""

UPDATE_CONSULTA = """
UPDATE consulta
SET idMedico = ?, idPaciente = ?, dataHora = ?, queixa = ?, conduta = ?
WHERE idConsulta = ?;
"""         

DELETAR_CONSULTA = """
DELETE FROM consulta
WHERE idConsulta = ?;
""" 
