CRIAR_TABELA_MEDICO = """
CREATE TABLE IF NOT EXISTS medico (
    idMedico INTEGER PRIMARY KEY,
    crm TEXT NOT NULL,
    statusProfissional TEXT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);
"""