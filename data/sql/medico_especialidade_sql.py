CRIAR_TABELA_MEDICO_ESPECIALIDADE = """
CREATE TABLE IF NOT EXISTS medico_especialidade (
    idMedico INTEGER NOT NULL,
    idEspecialidade INTEGER NOT NULL,
    dataHabilitacao TEXT NOT NULL,
    PRIMARY KEY (idMedico, idEspecialidade),
    FOREIGN KEY (idMedico) REFERENCES medico(idMedico),
    FOREIGN KEY (idEspecialidade) REFERENCES especialidade(idEspecialidade)
);
"""

INSERIR_MEDICO_ESPECIALIDADE = """
INSERT INTO medico_especialidade (idMedico, idEspecialidade, dataHabilitacao)
VALUES (?, ?, ?)
"""

OBTER_TODOS_MEDICOS_ESPECIALIDADES = """
SELECT 
m.idMedico, e.idEspecialidade, e.nome, e.descricao, me.dataHabilitacao
FROM medico_especialidade me
JOIN medico m ON me.idMedico = m.idMedico
JOIN especialidade e ON me.idEspecialidade = e.idEspecialidade
ORDER BY m.idMedico, e.idEspecialidade
"""

OBTER_MEDICO_ESPECIALIDADE_POR_ID = """
SELECT 
m.idMedico, e.idEspecialidade, e.nome, e.descricao, me.dataHabilitacao
FROM medico_especialidade me
JOIN medico m ON me.idMedico = m.idMedico
JOIN especialidade e ON me.idEspecialidade = e.idEspecialidade
WHERE m.idMedico = ? AND e.idEspecialidade = ?
"""

UPDATE_MEDICO_ESPECIALIDADE = """
UPDATE medico_especialidade
SET dataHabilitacao = ?
WHERE idMedico = ? AND idEspecialidade = ?
"""

DELETAR_MEDICO_ESPECIALIDADE = """
DELETE FROM medico_especialidade
WHERE idMedico = ? AND idEspecialidade = ?
"""
