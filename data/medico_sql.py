CRIAR_TABELA_MEDICO = """
CREATE TABLE IF NOT EXISTS medico (
idMedico INTEGER PRIMARY KEY,
crm TEXT NOT NULL,
statusProfissional TEXT NOT NULL,
FOREIGN KEY (idMedico) REFERENCES usuario(idUsuario)
);
"""

INSERIR_MEDICO = """
INSERT INTO medico (idMedico, crm, statusProfissional)
VALUES (?, ?, ?)
"""

OBTER_TODOS_MEDICOS = """
SELECT 
m.idMedico, u.nome, u.cpf,u.email, u.genero, u.dataNascimento, m.crm, m.statusProfissional
FROM medico m
JOIN usuario u ON m.idMedico = u.idUsuario
ORDER BY m.idMedico
"""

OBTER_MEDICOS_POR_ID = """
SELECT 
m.idMedico, u.nome, u.cpf,u.email, u.genero, u.dataNascimento, m.crm, m.statusProfissional
FROM medico m
JOIN usuario u ON m.idMedico = u.idUsuario
WHERE m.idMedico = ?
"""

UPDATE_MEDICO = """
UPDATE medico m
SET crm = ?, statusProfissional = ?
WHERE m.idMedico = ?
"""

DELETAR_MEDICO = """
DELETE FROM medico
WHERE idMedico = ?
"""