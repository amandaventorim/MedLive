CRIAR_TABELA_AGENDA = """
CREATE TABLE IF NOT EXISTS agenda (
    idAgenda INTEGER PRIMARY KEY AUTOINCREMENT,
    idEspecialidade INTEGER NOT NULL,
    dataHora TEXT NOT NULL,
    
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (idEspecialidade) REFERENCES especialidade(idEspecialidade)
);
"""