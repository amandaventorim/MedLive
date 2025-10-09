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

OBTER_AGENDAMENTOS_POR_PACIENTE = """
SELECT
a.idAgendamento, a.idPaciente, a.idMedico, a.dataAgendamento, a.horario, a.status, a.queixa, a.preco, a.dataInclusao,
u.nome as nomeMedico, m.crm, u.foto as fotoMedico
FROM agendamento a
JOIN usuario u ON a.idMedico = u.idUsuario
JOIN medico m ON a.idMedico = m.idMedico
WHERE a.idPaciente = ?
ORDER BY a.dataAgendamento DESC, a.horario DESC
"""

OBTER_AGENDAMENTOS_POR_MEDICO = """
SELECT
a.idAgendamento, a.idPaciente, a.idMedico, a.dataAgendamento, a.horario, a.status, a.queixa, a.preco, a.dataInclusao,
u.nome as nomePaciente, p.endereco, p.convenio, u.email as emailPaciente
FROM agendamento a
JOIN usuario u ON a.idPaciente = u.idUsuario
JOIN paciente p ON a.idPaciente = p.idPaciente
WHERE a.idMedico = ?
ORDER BY a.dataAgendamento DESC, a.horario DESC
"""

OBTER_AGENDAMENTOS_POR_MEDICO_SIMPLES = """
SELECT
a.idAgendamento, a.idPaciente, a.idMedico, a.dataAgendamento, a.horario, a.status, a.queixa, a.preco, a.dataInclusao
FROM agendamento a
WHERE a.idMedico = ?
ORDER BY a.dataAgendamento DESC, a.horario DESC
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
