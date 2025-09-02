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
a.idAdministrador, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento
FROM administrador a
JOIN usuario u ON a.idAdministrador = u.idUsuario
ORDER BY a.idAdministrador
"""

OBTER_ADMINISTRADORES_POR_PAGINA = """
SELECT
a.idAdministrador, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento
FROM administrador a
JOIN usuario u ON a.idAdministrador = u.idUsuario
ORDER BY a.idAdministrador
LIMIT ? OFFSET ?
"""

OBTER_ADMINISTRADOR_POR_ID = """
SELECT 
a.idAdministrador, u.nome, u.cpf, u.email, u.senha, u.genero, u.dataNascimento
FROM administrador a
JOIN usuario u ON a.idAdministrador = u.idUsuario
WHERE a.idAdministrador = ?
"""
# Não tem o que atualizar na tabela administrador, pois ela só referencia o idUsuario.
# UPDATE_ADMINISTRADOR = """
# UPDATE administrador
# SET idAdministrador = ?
# WHERE idAdministrador = ?
# """

DELETAR_ADMINISTRADOR = """
DELETE FROM administrador
WHERE idAdministrador = ?
"""
