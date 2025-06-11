CRIAR_TABELA_PACIENTE = """
CREATE TABLE IF NOT EXISTS paciente (
    idPaciente INTEGER PRIMARY KEY,
    endereco TEXT NOT NULL,
    convenio TEXT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);
"""