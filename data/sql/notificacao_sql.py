CREATE_TABLE_NOTIFICACOES = """
CREATE TABLE IF NOT EXISTS notificacoes (
    idNotificacao INTEGER PRIMARY KEY AUTOINCREMENT,
    idUsuario INTEGER NOT NULL,
    tipoUsuario TEXT NOT NULL CHECK (tipoUsuario IN ('medico', 'paciente')),
    tipo TEXT NOT NULL,
    titulo TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    lida INTEGER DEFAULT 0 CHECK (lida IN (0, 1)),
    dataInclusao DATETIME DEFAULT CURRENT_TIMESTAMP,
    dadosAdicionais TEXT,
    acaoRequerida INTEGER DEFAULT 0 CHECK (acaoRequerida IN (0, 1)),
    expiresAt DATETIME
);
"""

CREATE_INDEXES_NOTIFICACOES = """
CREATE INDEX IF NOT EXISTS idx_usuario_tipo ON notificacoes (idUsuario, tipoUsuario);
CREATE INDEX IF NOT EXISTS idx_lida ON notificacoes (lida);
CREATE INDEX IF NOT EXISTS idx_data_inclusao ON notificacoes (dataInclusao);
"""

INSERT_NOTIFICACAO = """
INSERT INTO notificacoes (idUsuario, tipoUsuario, tipo, titulo, mensagem, lida, dadosAdicionais, acaoRequerida, expiresAt)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_NOTIFICACOES_POR_USUARIO = """
SELECT * FROM notificacoes 
WHERE idUsuario = ? AND tipoUsuario = ? 
ORDER BY dataInclusao DESC 
LIMIT ? OFFSET ?
"""

SELECT_NOTIFICACOES_NAO_LIDAS = """
SELECT * FROM notificacoes 
WHERE idUsuario = ? AND tipoUsuario = ? AND lida = 0
ORDER BY dataInclusao DESC
"""

COUNT_NOTIFICACOES_NAO_LIDAS = """
SELECT COUNT(*) as total FROM notificacoes 
WHERE idUsuario = ? AND tipoUsuario = ? AND lida = 0
"""

UPDATE_NOTIFICACAO_LIDA = """
UPDATE notificacoes 
SET lida = 1 
WHERE idNotificacao = ? AND idUsuario = ? AND tipoUsuario = ?
"""

UPDATE_TODAS_NOTIFICACOES_LIDAS = """
UPDATE notificacoes 
SET lida = 1 
WHERE idUsuario = ? AND tipoUsuario = ? AND lida = 0
"""

DELETE_NOTIFICACAO = """
DELETE FROM notificacoes 
WHERE idNotificacao = ? AND idUsuario = ? AND tipoUsuario = ?
"""

DELETE_NOTIFICACOES_EXPIRADAS = """
DELETE FROM notificacoes 
WHERE expiresAt IS NOT NULL AND expiresAt < CURRENT_TIMESTAMP
"""

SELECT_NOTIFICACAO_POR_ID = """
SELECT * FROM notificacoes 
WHERE idNotificacao = ? AND idUsuario = ? AND tipoUsuario = ?
"""