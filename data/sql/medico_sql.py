CRIAR_TABELA_MEDICO = """
CREATE TABLE IF NOT EXISTS medico (
    idMedico INTEGER PRIMARY KEY,
    crm TEXT NOT NULL,
    statusProfissional TEXT NOT NULL,
    FOREIGN KEY (idMedico) REFERENCES usuario(idUsuario) # é necessário o idUsuario? o medico tem dois ids? idmedico e idusuario ou só idmedico? idmedico é igual a idusuario?
);
"""

