import os
import sys
from data.model.medico_model import Medico
from data.repo.medico_repo import *
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario, obter_usuario_por_id
from tests.conftest import lista_medicos_exemplo, medico_exemplo, usuario_exemplo

class TestMedicoRepo:
    def test_criar_tabela_medico(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_medico()
        # Assert
        assert resultado == True, "A criação da tabela 'medico' falhou."

    def test_inserir_medico(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        medico_teste = Medico(0, "Carlos", "12345678900", "carlos@email.com", "senha123", "Masculino", "1980-01-01", 0, "CRM123", "Ativo")
        # Act
        id_medico_inserido = inserir_medico(medico_teste)
        # Assert
        medico_db = obter_medico_por_id(id_medico_inserido)
        assert medico_db is not None, "O médico inserido não foi encontrado."
        usuario_db = obter_usuario_por_id(medico_db.idUsuario)
        assert usuario_db is not None, "O usuário do médico inserido não foi encontrado."
        assert usuario_db.nome == "Carlos", "O nome do médico inserido deve ser igual ao nome inserido"
        assert usuario_db.cpf == "12345678900", "O CPF do médico inserido deve ser igual ao CPF inserido"
        assert usuario_db.email == "carlos@email.com", "O email do médico inserido deve ser igual ao email inserido"
        assert usuario_db.senha == "senha123", "A senha do médico inserido deve ser igual à senha inserida"
        assert usuario_db.genero == "Masculino", "O gênero do médico inserido deve ser igual ao gênero inserido"
        assert usuario_db.dataNascimento == "1980-01-01", "A data de nascimento do médico inserido deve ser igual à data de nascimento inserida"
        assert medico_db.crm == "CRM123", "O CRM do médico inserido deve ser igual ao CRM inserido"
        assert medico_db.statusProfissional == "Ativo", "O status profissional do médico inserido deve ser igual ao status inserido"

    def test_obter_todos_medicos(self, test_db, lista_medicos_exemplo):
    # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        for i, medico in enumerate(lista_medicos_exemplo):
            id_inserido = inserir_medico(medico)
            medico.idUsuario = id_inserido
            medico.idMedico = id_inserido
        # Act
        medicos = obter_todos_medicos()
        # Assert
        assert len(medicos) == len(lista_medicos_exemplo), "O número de médicos obtidos não corresponde ao número de médicos inseridos."
        for i, medico in enumerate(medicos):
            assert medico.idMedico == lista_medicos_exemplo[i].idMedico, f"O ID do médico {i} obtido não corresponde ao ID do médico inserido."
            assert medico.idUsuario == lista_medicos_exemplo[i].idUsuario, f"O ID do usuário do médico {i} obtido não corresponde ao ID do usuário inserido."
            assert medico.nome == lista_medicos_exemplo[i].nome, f"O nome do médico {i} obtido não corresponde ao nome do médico inserido."
            assert medico.cpf == lista_medicos_exemplo[i].cpf, f"O CPF do médico {i} obtido não corresponde ao CPF do médico inserido."
            assert medico.email == lista_medicos_exemplo[i].email, f"O email do médico {i} obtido não corresponde ao email do médico inserido."
            assert medico.senha == lista_medicos_exemplo[i].senha, f"A senha do médico {i} obtido não corresponde à senha do médico inserida."
            assert medico.genero == lista_medicos_exemplo[i].genero, f"O gênero do médico {i} obtido não corresponde ao gênero inserido."
            assert medico.dataNascimento == lista_medicos_exemplo[i].dataNascimento, f"A data de nascimento do médico {i} obtido não corresponde à data inserida."
            assert medico.crm == lista_medicos_exemplo[i].crm, f"O CRM do médico {i} obtido não corresponde ao CRM inserido."
            assert medico.statusProfissional == lista_medicos_exemplo[i].statusProfissional, f"O status profissional do médico {i} obtido não corresponde ao inserido."


    def test_obter_medicos_por_pagina(self, test_db, lista_medicos_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        medicos_inseridos = []
        for medico in lista_medicos_exemplo:
            id_inserido = inserir_medico(medico)
            medico_inserido = obter_medico_por_id(id_inserido)
            medicos_inseridos.append(medico_inserido)

        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        medicos = obter_medicos_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(medicos) == tamanho_pagina, "O número de médicos obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, medico in enumerate(medicos):
            esperado = medicos_inseridos[start_index + i]
            assert medico.idMedico == esperado.idMedico, f"O ID do médico {i} obtido não corresponde ao ID do médico inserido."
            assert medico.idUsuario == esperado.idUsuario, f"O ID do usuário do médico {i} obtido não corresponde ao ID do usuário inserido."
            assert medico.nome == esperado.nome, f"O nome do médico {i} obtido não corresponde ao nome do médico inserido."
            assert medico.cpf == esperado.cpf, f"O CPF do médico {i} obtido não corresponde ao CPF do médico inserido."
            assert medico.email == esperado.email, f"O email do médico {i} obtido não corresponde ao email do médico inserido."
            assert medico.senha == esperado.senha, f"A senha do médico {i} obtido não corresponde à senha do médico inserido."
            assert medico.genero == esperado.genero, f"O gênero do médico {i} obtido não corresponde ao gênero do médico inserido."
            assert medico.dataNascimento == esperado.dataNascimento, f"A data de nascimento do médico {i} obtido não corresponde à data de nascimento do médico inserido."
            assert medico.crm == esperado.crm, f"O CRM do médico {i} obtido não corresponde ao CRM do médico inserido."
            assert medico.statusProfissional == esperado.statusProfissional, f"O status profissional do médico {i} obtido não corresponde ao status profissional do médico inserido."


    def test_obter_medico_por_id(self, test_db, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        id_medico = inserir_medico(medico_exemplo)
        # Act
        medico_obtido = obter_medico_por_id(id_medico)
        # Assert
        assert medico_obtido is not None, "O médico obtido não deve ser None."
        assert medico_obtido.idMedico == id_medico, "O ID do médico obtido não corresponde ao ID do médico inserido."
        assert medico_obtido.idUsuario == id_medico, "O ID do usuário do médico obtido não corresponde ao ID do médico inserido."
        assert medico_obtido.nome == medico_exemplo.nome, "O nome do médico obtido não corresponde ao nome do médico inserido."
        assert medico_obtido.cpf == medico_exemplo.cpf, "O CPF do médico obtido não corresponde ao CPF do médico inserido."
        assert medico_obtido.email == medico_exemplo.email, "O email do médico obtido não corresponde ao email do médico inserido."
        assert medico_obtido.senha == medico_exemplo.senha, "A senha do médico obtido não corresponde à senha do médico inserida."
        assert medico_obtido.genero == medico_exemplo.genero, "O gênero do médico obtido não corresponde ao gênero do médico inserido."
        assert medico_obtido.dataNascimento == medico_exemplo.dataNascimento, "A data de nascimento do médico obtido não corresponde à data de nascimento do médico inserida."
        assert medico_obtido.crm == medico_exemplo.crm, "O CRM do médico obtido não corresponde ao CRM do médico inserido."
        assert medico_obtido.statusProfissional == medico_exemplo.statusProfissional, "O status profissional do médico obtido não corresponde ao status profissional do médico inserido."


    def test_obter_medico_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        # Act
        medico = obter_medico_por_id(9999)
        # Assert
        assert medico is None, "O médico obtido deve ser None para um ID inexistente."

    def test_atualizar_medico(self, test_db, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        id_medico = inserir_medico(medico_exemplo)

        medico_exemplo.idMedico = id_medico
        medico_exemplo.idUsuario = id_medico
        medico_exemplo.nome = "Novo Nome Médico"
        medico_exemplo.cpf = "98765432100"
        medico_exemplo.email = "novoemail@medico.com"
        medico_exemplo.genero = "Feminino"
        medico_exemplo.dataNascimento = "1990-01-01"
        medico_exemplo.crm = "CRM-99999"
        medico_exemplo.statusProfissional = "Inativo"
        # Act
        resultado = atualizar_medico(medico_exemplo)
        # Assert
        assert resultado == True, "A atualização do médico falhou."
        usuario_atualizado = obter_usuario_por_id(medico_exemplo.idUsuario)
        assert usuario_atualizado.nome == "Novo Nome Médico", "O nome do usuário atualizado não corresponde ao novo nome."
        assert usuario_atualizado.cpf == "98765432100", "O CPF do usuário atualizado não corresponde ao novo CPF."
        assert usuario_atualizado.email == "novoemail@medico.com", "O email do usuário atualizado não corresponde ao novo email."
        assert usuario_atualizado.genero == "Feminino", "O gênero do usuário atualizado não corresponde ao novo gênero."
        assert usuario_atualizado.dataNascimento == "1990-01-01", "A data de nascimento do usuário atualizado não corresponde à nova data de nascimento."
        medico_atualizado = obter_medico_por_id(id_medico)
        assert medico_atualizado.crm == "CRM-99999", "O CRM do médico atualizado não corresponde ao novo CRM."
        assert medico_atualizado.statusProfissional == "Inativo", "O status profissional do médico atualizado não corresponde ao novo status."

    def test_atualizar_senha_medico(self, test_db, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        id_medico = inserir_medico(medico_exemplo)
        senha_antiga = medico_exemplo.senha
        nova_senha = "novaSenha456"
        usuario_antes = obter_usuario_por_id(id_medico)
        # Act
        resultado = atualizar_senha_medico(id_medico, nova_senha)
        # Assert
        assert resultado == True, "A atualização da senha do médico falhou."
        usuario_atualizado = obter_usuario_por_id(id_medico)
        assert usuario_atualizado.senha == nova_senha, "A senha do usuário atualizado não corresponde à nova senha."


    def test_atualizar_senha_medico_inexistente(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        id_medico_inexistente = id_usuario_inserido
        nova_senha = "novaSenha456"
        # Act
        resultado = atualizar_senha_medico(id_medico_inexistente, "senhaInvalida")
        # Assert
        assert resultado == False

    def test_deletar_usuario_medico(self, test_db, medico_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_medico()
        id_medico = inserir_medico(medico_exemplo)
        # Act
        resultado = deletar_usuario_medico(id_medico)
        # Assert
        assert resultado == True, "A exclusão do médico falhou."
        assert obter_medico_por_id(id_medico) is None, "O médico não deve ser encontrado após a exclusão."
        assert obter_usuario_por_id(id_medico) is None, "O usuário do médico não deve ser encontrado após a exclusão."




