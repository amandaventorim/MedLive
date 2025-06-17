CRIAR_TABELA_AGENDA = """
CREATE TABLE IF NOT EXISTS agenda (
    idAgenda INTEGER PRIMARY KEY AUTOINCREMENT,
    idMedico INTEGER NOT NULL,
    dataHora TEXT NOT NULL,
    disponivel BOOLEAN NOT NULL
    FOREIGN KEY (idMedico) REFERENCES medico(idMedico)
);
"""

INSERIR_AGENDA = """
INSERT INTO agenda (idMedico, dataHora, disponivel) 
VALUES (?, ?, ?)
"""

OBTER_TODAS_AGENDAS = """
SELECT
idAgenda, idMedico, dataHora, disponivel
FROM agenda
ORDER BY idAgenda
"""

OBTER_AGENDA_POR_ID = """
SELECT
idAgenda, idMedico, dataHora, disponivel
FROM agenda
WHERE idAgenda = ?
"""

UPDATE_AGENDA = """
UPDATE agenda
SET idMedico = ?, dataHora = ?, disponivel = ?
WHERE idAgenda = ?
"""

DELETAR_AGENDA = """
DELETE FROM agenda
WHERE idAgenda = ?
"""

