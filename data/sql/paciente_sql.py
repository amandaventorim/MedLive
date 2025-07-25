CRIAR_TABELA_PACIENTE = """
CREATE TABLE IF NOT EXISTS paciente (
idPaciente INTEGER PRIMARY KEY,
endereco TEXT NOT NULL,
convenio TEXT NOT NULL,
FOREIGN KEY (idPaciente) REFERENCES usuario(idUsuario)
);
"""

INSERIR_PACIENTE = """
INSERT INTO paciente (idPaciente, endereco, convenio)
VALUES (?, ?, ?)
"""

OBTER_TODOS_PACIENTES = """
SELECT 
p.idPaciente, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento, p.endereco, p.convenio
FROM paciente p
JOIN usuario u ON p.idPaciente = u.idUsuario
ORDER BY p.idPaciente
"""

OBTER_PACIENTES_POR_PAGINA = """
SELECT
p.idPaciente, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento, p.endereco, p.convenio
FROM paciente p
JOIN usuario u ON p.idPaciente = u.idUsuario
ORDER BY p.idPaciente
LIMIT ? OFFSET ?
"""

OBTER_PACIENTE_POR_ID = """
SELECT 
p.idPaciente, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento, p.endereco, p.convenio
FROM paciente p
JOIN usuario u ON p.idPaciente = u.idUsuario
WHERE p.idPaciente = ?
"""

UPDATE_PACIENTE = """
UPDATE paciente
SET endereco = ?, convenio = ?
WHERE idPaciente = ?
"""

DELETAR_PACIENTE = """
DELETE FROM paciente
WHERE idPaciente = ?
"""

