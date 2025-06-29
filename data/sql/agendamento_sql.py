CRIAR_TABELA_AGENDAMENTO = """
CREATE TABLE IF NOT EXISTS agendamento (
idAgendamento INTEGER PRIMARY KEY,
idPaciente INTEGER NOT NULL,
status TEXT NOT NULL,
dataAgendamento TEXT NOT NULL,
FOREIGN KEY (idAgendamento) REFERENCES agenda(idAgenda),
FOREIGN KEY (idPaciente) REFERENCES paciente(idPaciente)
);
"""

INSERIR_AGENDAMENTO = """
INSERT INTO agendamento (idPaciente, status, dataAgendamento)
VALUES (?, ?, ?)
"""

OBTER_TODOS_AGENDAMENTOS = """
SELECT
idAgendamento, idPaciente, status, dataAgendamento
FROM agendamento 
ORDER BY idAgendamento
"""

OBTER_AGENDAMENTOS_POR_PAGINA = """
SELECT
idAgendamento, idPaciente, status, dataAgendamento
FROM agendamento
ORDER BY idAgendamento
LIMIT ? OFFSET ?
"""

OBTER_AGENDAMENTO_POR_ID = """
SELECT
idAgendamento, idPaciente, status, dataAgendamento
FROM agendamento
WHERE idAgendamento = ?
"""

UPDATE_AGENDAMENTO = """
UPDATE agendamento
SET idPaciente = ?, status = ?, dataAgendamento = ?
WHERE idAgendamento = ?
"""

DELETAR_AGENDAMENTO = """
DELETE FROM agendamento
WHERE idAgendamento = ?
"""
