CRIAR_TABELA_ITEM_RECEITA = """
CREATE TABLE IF NOT EXISTS item_receita (     
idConsulta INTEGER NOT NULL,
idMedicamento INTEGER NOT NULL,
descricao TEXT NOT NULL,
PRIMARY KEY (idConsulta, idMedicamento),
FOREIGN KEY (idConsulta) REFERENCES consulta(idConsulta),
FOREIGN KEY (idMedicamento) REFERENCES medicamento(idMedicamento)
);
"""

INSERIR_ITEM_RECEITA = """
INSERT INTO item_receita (idConsulta, idMedicamento, descricao)   
VALUES (?, ?, ?)
"""

OBTER_TODOS_ITENS_RECEITA = """
SELECT
idConsulta, idMedicamento, descricao
FROM item_receita
"""

OBTER_ITEM_RECEITA_POR_ID = """
SELECT  
idConsulta, idMedicamento, descricao
FROM item_receita
WHERE idConsulta = ? AND idMedicamento = ?
""" 

UPDATE_ITEM_RECEITA = """
UPDATE item_receita
SET descricao = ?
WHERE idConsulta = ? AND idMedicamento = ?
"""

DELETAR_ITEM_RECEITA = """
DELETE FROM item_receita
WHERE idConsulta = ? AND idMedicamento = ?
""" 

