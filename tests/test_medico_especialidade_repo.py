import os
import sys
from data.repo.medico_especialidade_repo import *
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.repo.medico_repo import criar_tabela_medico, inserir_medico
from data.repo.especialidade_repo import criar_tabela_especialidade, inserir_especialidade
from data.repo.usuario_repo import criar_tabela_usuario
from tests.conftest import medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo

class TestMedicoEspecialidadeRepo:
    def test_criar_tabela_medico_especialidade(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        # Act
        resultado = criar_tabela_medico_especialidade()
        # Assert
        assert resultado == True, "A criação da tabela 'medico_especialidade' falhou."

    def test_inserir_medico_especialidade(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idMedico = id_medico_inserido
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida
        # Act
        resultado = inserir_medico_especialidade(medico_especialidade_exemplo)
        # Assert
        assert resultado == True, "A inserção da relação médico-especialidade falhou."
        medico_especialidade_db = obter_medico_especialidade_por_id(id_medico_inserido, id_especialidade_inserida)
        assert medico_especialidade_db is not None, "A relação médico-especialidade inserida não foi encontrada no banco de dados."
        assert medico_especialidade_db.idMedico == id_medico_inserido, "O ID do médico da relação inserida está incorreto."
        assert medico_especialidade_db.idEspecialidade == id_especialidade_inserida, "O ID da especialidade da relação inserida está incorreto."
        assert medico_especialidade_db.dataHabilitacao == medico_especialidade_exemplo.dataHabilitacao, "A data de habilitação da relação inserida está incorreta."

    def test_obter_todos_medicos_especialidades(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_especialidade_inserida1 = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idMedico = id_medico_inserido
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida1
        inserir_medico_especialidade(medico_especialidade_exemplo)
        especialidade_exemplo.nome = "Especialidade 2"
        especialidade_exemplo.descricao = "Descrição 2"
        id_especialidade_inserida2 = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida2
        inserir_medico_especialidade(medico_especialidade_exemplo)
        # Act
        medicos_especialidades = obter_todos_medicos_especialidades()
        # Assert
        assert len(medicos_especialidades) == 2, "O número de relações médico-especialidade obtidas não é igual a 2."
        assert medicos_especialidades[0].idMedico == id_medico_inserido, "O ID do médico da primeira relação não é o esperado."
        assert medicos_especialidades[0].idEspecialidade == id_especialidade_inserida1, "O ID da especialidade da primeira relação não é o esperado."
        assert medicos_especialidades[1].idMedico == id_medico_inserido, "O ID do médico da segunda relação não é o esperado."
        assert medicos_especialidades[1].idEspecialidade == id_especialidade_inserida2, "O ID da especialidade da segunda relação não é o esperado."

    def test_obter_medico_especialidade_por_id(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idMedico = id_medico_inserido
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida
        inserir_medico_especialidade(medico_especialidade_exemplo)
        # Act
        medico_especialidade_db = obter_medico_especialidade_por_id(id_medico_inserido, id_especialidade_inserida)
        # Assert
        assert medico_especialidade_db is not None, "A relação médico-especialidade não foi encontrada no banco de dados."
        assert medico_especialidade_db.idMedico == id_medico_inserido, "O ID do médico da relação obtida não é o esperado."
        assert medico_especialidade_db.idEspecialidade == id_especialidade_inserida, "O ID da especialidade da relação obtida não é o esperado."

    def test_obter_medico_especialidade_por_pagina(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        total_registros = 10
        for i in range(total_registros):
            especialidade_exemplo.nome = f"Especialidade {i+1}"
            especialidade_exemplo.descricao = f"Descrição {i+1}"
            id_especialidade = inserir_especialidade(especialidade_exemplo)

            medico_especialidade_exemplo.idMedico = id_medico_inserido
            medico_especialidade_exemplo.idEspecialidade = id_especialidade
            inserir_medico_especialidade(medico_especialidade_exemplo)
        numero_pagina = 2
        tamanho_pagina = 3
        # Act
        resultado = obter_medicos_especialidades_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(resultado) == tamanho_pagina, "A quantidade de registros retornados não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, relacao in enumerate(resultado):
            index = start_index + i
            assert relacao.idMedico == id_medico_inserido, f"O ID do médico na relação {i} não é o esperado."
            assert relacao.idEspecialidade > 0, f"O ID da especialidade na relação {i} não é válido."
            assert isinstance(relacao.dataHabilitacao, str), f"A data de habilitação da relação {i} deve ser uma string."


    def test_atualizar_medico_especialidade(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idMedico = id_medico_inserido
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida
        inserir_medico_especialidade(medico_especialidade_exemplo)
        medico_especialidade_inserida = obter_medico_especialidade_por_id(id_medico_inserido, id_especialidade_inserida)
        # Act
        medico_especialidade_inserida.dataHabilitacao = "2024-01-01"
        resultado = atualizar_medico_especialidade(medico_especialidade_inserida)
        # Assert
        assert resultado == True, "A atualização da relação médico-especialidade falhou."
        medico_especialidade_db = obter_medico_especialidade_por_id(id_medico_inserido, id_especialidade_inserida)
        assert medico_especialidade_db.dataHabilitacao == "2024-01-01", "A data de habilitação da relação não foi alterada corretamente."

    def test_deletar_medico_especialidade(self, test_db, medico_especialidade_exemplo, medico_exemplo, especialidade_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        criar_tabela_especialidade()
        criar_tabela_medico_especialidade()
        id_medico_inserido = inserir_medico(medico_exemplo)
        id_especialidade_inserida = inserir_especialidade(especialidade_exemplo)
        medico_especialidade_exemplo.idMedico = id_medico_inserido
        medico_especialidade_exemplo.idEspecialidade = id_especialidade_inserida
        inserir_medico_especialidade(medico_especialidade_exemplo)
        # Act
        resultado = deletar_medico_especialidade(id_medico_inserido, id_especialidade_inserida)
        # Assert
        assert resultado == True, "A exclusão da relação médico-especialidade falhou."
        medico_especialidade_db = obter_medico_especialidade_por_id(id_medico_inserido, id_especialidade_inserida)
        assert medico_especialidade_db == None, "A relação médico-especialidade ainda existe no banco de dados após a exclusão."


