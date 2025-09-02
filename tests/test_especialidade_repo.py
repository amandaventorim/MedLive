import os
import sys
from data.repo.especialidade_repo import *
from data.model.especialidade_model import Especialidade
from tests.conftest import especialidade_exemplo, lista_especialidades_exemplo

class TestEspecialidadeRepo:
    def test_criar_tabela_especialidade(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'especialidade' falhou."

    def test_inserir_especialidade(self, test_db, especialidade_exemplo):
        # Arrange
        criar_tabela_especialidade()
        # Act
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        # Assert
        especialidade_db = obter_especialidade_por_id(id_especialidade_inserida)
        assert especialidade_db is not None, "A especialidade inserida não foi encontrada no banco de dados."
        assert especialidade_db.idEspecialidade == 1, "O ID da especialidade inserida deve ser igual a 1"
        assert especialidade_db.nome == especialidade_exemplo.nome, "O nome da especialidade inserida está incorreto"
        assert especialidade_db.descricao == especialidade_exemplo.descricao, "A descrição da especialidade inserida está incorreta"

    def test_obter_todas_especialidades(self, test_db, especialidade_exemplo):
        # Arrange
        criar_tabela_especialidade()
        inserir_especialidade(especialidade_exemplo)
        especialidade_exemplo.nome = "Especialidade 2"
        inserir_especialidade(especialidade_exemplo)
        # Act
        especialidades = obter_todas_especialidades()
        # Assert
        assert len(especialidades) == 2, "O número de especialidades obtidas não é igual a 2."
        assert especialidades[0].idEspecialidade == 1, "O ID da primeira especialidade não é o esperado."
        assert especialidades[1].idEspecialidade == 2, "O ID da segunda especialidade não é o esperado."

    def test_obter_especialidades_por_pagina(self, test_db, lista_especialidades_exemplo):
        # Arrange
        criar_tabela_especialidade()
        for especialidade in lista_especialidades_exemplo:
            inserir_especialidade(especialidade)
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        especialidades = obter_especialidades_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(especialidades) == tamanho_pagina, "O número de especialidades obtidas por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, especialidade in enumerate(especialidades):
            esperado = lista_especialidades_exemplo[start_index + i]
            assert especialidade.idEspecialidade == esperado.idEspecialidade, f"O ID da especialidade {i} obtida não corresponde ao esperado."
            assert especialidade.nome == esperado.nome, f"O nome da especialidade {i} obtida não corresponde ao esperado."
            assert especialidade.descricao == esperado.descricao, f"A descrição da especialidade {i} obtida não corresponde à esperada."

    def test_obter_especialidade_por_id(self, test_db, especialidade_exemplo):
        # Arrange
        criar_tabela_especialidade()
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        # Act
        especialidade_db = obter_especialidade_por_id(id_especialidade_inserida)
        # Assert
        assert especialidade_db is not None, "A especialidade não foi encontrada no banco de dados."
        assert especialidade_db.idEspecialidade == id_especialidade_inserida, "O ID da especialidade obtida não é o esperado."

    def test_atualizar_especialidade(self, test_db, especialidade_exemplo):
        # Arrange
        criar_tabela_especialidade()
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        especialidade_inserida = obter_especialidade_por_id(id_especialidade_inserida)
        # Act
        especialidade_inserida.nome = "Nova Especialidade"
        especialidade_inserida.descricao = "Nova Descrição"
        resultado = atualizar_especialidade(especialidade_inserida)
        # Assert
        assert resultado == True, "A atualização da especialidade falhou."
        especialidade_db = obter_especialidade_por_id(id_especialidade_inserida)
        assert especialidade_db.nome == "Nova Especialidade", "O nome da especialidade não foi alterado corretamente."
        assert especialidade_db.descricao == "Nova Descrição", "A descrição da especialidade não foi alterada corretamente."

    def test_deletar_especialidade(self, test_db, especialidade_exemplo):
        # Arrange
        criar_tabela_especialidade()
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        # Act
        resultado = deletar_especialidade(id_especialidade_inserida)
        # Assert
        assert resultado == True, "A exclusão da especialidade falhou."
        especialidade_db = obter_especialidade_por_id(id_especialidade_inserida)
        assert especialidade_db == None, "A especialidade ainda existe no banco de dados após a exclusão."


