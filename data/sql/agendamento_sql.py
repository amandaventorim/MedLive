CRIAR_TABELA_AGENDAMENTO = """
CREATE TABLE IF NOT EXISTS agendamento (
idAgendamento INTEGER PRIMARY KEY,
idPaciente INTEGER NOT NULL,
idMedico INTEGER NOT NULL,
dataAgendamento TEXT NOT NULL,
horario TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'agendado',
queixa TEXT,
preco REAL DEFAULT 0.0,
dataInclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (idPaciente) REFERENCES usuario(idUsuario),
FOREIGN KEY (idMedico) REFERENCES usuario(idUsuario)
);
"""

INSERIR_AGENDAMENTO = """
INSERT INTO agendamento (idPaciente, idMedico, dataAgendamento, horario, status, queixa, preco)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

OBTER_TODOS_AGENDAMENTOS = """
SELECT
idAgendamento, idPaciente, idMedico, dataAgendamento, horario, status, queixa, preco, dataInclusao
FROM agendamento 
ORDER BY idAgendamento
"""

OBTER_AGENDAMENTOS_POR_PAGINA = """
SELECT
idAgendamento, idPaciente, idMedico, dataAgendamento, horario, status, queixa, preco, dataInclusao
FROM agendamento
ORDER BY idAgendamento
LIMIT ? OFFSET ?
"""

OBTER_AGENDAMENTO_POR_ID = """
SELECT
idAgendamento, idPaciente, idMedico, dataAgendamento, horario, status, queixa, preco, dataInclusao
FROM agendamento
WHERE idAgendamento = ?
"""

UPDATE_AGENDAMENTO = """
UPDATE agendamento
SET idPaciente = ?, idMedico = ?, dataAgendamento = ?, horario = ?, status = ?, queixa = ?, preco = ?
WHERE idAgendamento = ?
"""

DELETAR_AGENDAMENTO = """
DELETE FROM agendamento
WHERE idAgendamento = ?
"""
