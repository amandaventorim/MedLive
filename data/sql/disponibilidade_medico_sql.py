CRIAR_TABELA_DISPONIBILIDADE_MEDICO = """
CREATE TABLE IF NOT EXISTS disponibilidade_medico (
    idDisponibilidade INTEGER PRIMARY KEY AUTOINCREMENT,
    idMedico INTEGER NOT NULL,
    diaSemana INTEGER NOT NULL CHECK (diaSemana >= 1 AND diaSemana <= 7),
    horaInicio TEXT NOT NULL,
    horaFim TEXT NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT 1,
    dataInclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idMedico) REFERENCES medico(idMedico),
    UNIQUE(idMedico, diaSemana, horaInicio, horaFim)
);
"""

INSERIR_DISPONIBILIDADE_MEDICO = """
INSERT INTO disponibilidade_medico (idMedico, diaSemana, horaInicio, horaFim, ativo)
VALUES (?, ?, ?, ?, ?)
"""

OBTER_DISPONIBILIDADES_POR_MEDICO = """
SELECT
idDisponibilidade, idMedico, diaSemana, horaInicio, horaFim, ativo, dataInclusao
FROM disponibilidade_medico
WHERE idMedico = ?
ORDER BY diaSemana, horaInicio
"""

OBTER_DISPONIBILIDADE_POR_ID = """
SELECT
idDisponibilidade, idMedico, diaSemana, horaInicio, horaFim, ativo, dataInclusao
FROM disponibilidade_medico
WHERE idDisponibilidade = ?
"""

ATUALIZAR_DISPONIBILIDADE_MEDICO = """
UPDATE disponibilidade_medico
SET diaSemana = ?, horaInicio = ?, horaFim = ?, ativo = ?
WHERE idDisponibilidade = ?
"""

DELETAR_DISPONIBILIDADE_MEDICO = """
DELETE FROM disponibilidade_medico
WHERE idDisponibilidade = ?
"""

DELETAR_TODAS_DISPONIBILIDADES_MEDICO = """
DELETE FROM disponibilidade_medico
WHERE idMedico = ?
"""
