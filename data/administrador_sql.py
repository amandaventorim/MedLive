CRIAR_TABELA_ADMINISTRADOR = """
CREATE TABLE IF NOT EXISTS administrador (
idAdministrador INTEGER PRIMARY KEY,
FOREIGN KEY (idAdministrador) REFERENCES usuario(idUsuario)
);
"""

INSERIR_ADMINISTRADOR = """
INSERT INTO administrador (idAdministrador)
VALUES (?)
"""

OBTER_TODOS_ADMINISTRADORES = """
SELECT 
a.idAdministrador, u.nome, u.cpf, u.email, u.genero, u.dataNascimento, a.cargo
FROM administrador a
JOIN usuario u ON a.idUsuario = u.idUsuario
ORDER BY a.idAdministrador
"""

OBTER_ADMINISTRADOR_POR_ID = """
SELECT 
a.idAdministrador, u.nome, u.cpf, u.email, u.genero, u.dataNascimento, a.cargo
FROM administrador a
JOIN usuario u ON a.idUsuario = u.idUsuario
WHERE a.idAdministrador = ?
"""

UPDATE_ADMINISTRADOR = """
UPDATE administrador a
SET idUsuario = ?, cargo = ?
WHERE a.idAdministrador = ?
"""

DELETAR_ADMINISTRADOR = """
DELETE FROM administrador
WHERE idAdministrador = ?
"""
