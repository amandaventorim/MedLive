import os
import sys
from data.repo.administrador_repo import *
from data.model.administrador_model import Administrador
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario, obter_usuario_por_id
from tests.conftest import administrador_exemplo, usuario_exemplo, lista_administradores_exemplo

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_administrador()
        # Assert
        assert resultado == True, "A criação da tabela 'administrador' falhou."

    def test_inserir_administrador(self, test_db, administrador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        # Act
        id_administrador_inserido = inserir_administrador(administrador_exemplo)
        # Assert
        administrador_db = obter_administrador_por_id(id_administrador_inserido)
        assert administrador_db is not None, "O administrador inserido não foi encontrado na tabela administrador do banco de dados."
        usuario_db = obter_usuario_por_id(administrador_db.idUsuario)
        assert usuario_db is not None, "O usuário do administrador não foi encontrado na tabela usuario."
        assert administrador_db.idAdministrador == 1, "O ID do administrador inserido deve ser igual a 1"
        assert administrador_db.idUsuario == 1, "O ID do usuário do administrador inserido deve ser igual a 1"
        assert usuario_db.nome == "admin_teste", "O nome do administrador inserido está incorreto"
        assert usuario_db.cpf == "11122233344", "O CPF do administrador inserido está incorreto"
        assert usuario_db.email == "admin@email.com", "O email do administrador inserido está incorreto"
        assert usuario_db.senha == "admin123", "A senha do administrador inserido está incorreta"
        assert usuario_db.genero == "Masculino", "O gênero do administrador inserido está incorreto"
        assert usuario_db.dataNascimento == "2000-01-01", "A data de nascimento do administrador inserido está incorreta"

    def test_obter_todos_administradores(self, test_db, lista_administradores_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        for i, administrador in enumerate(lista_administradores_exemplo):
            id_inserido = inserir_administrador(administrador)
            administrador.idUsuario = id_inserido
            administrador.idAdministrador = id_inserido
        # Act
        administradores = obter_todos_administradores()
        # Assert
        assert len(administradores) == len(lista_administradores_exemplo), "O número de administradores obtidos não corresponde ao número de administradores inseridos."
        for i, administrador in enumerate(administradores):
            esperado = lista_administradores_exemplo[i]
            assert administrador.idAdministrador == esperado.idAdministrador, f"O ID do administrador {i} obtido não corresponde ao esperado."
            assert administrador.idUsuario == esperado.idUsuario, f"O ID do usuário do administrador {i} obtido não corresponde ao esperado."
            assert administrador.nome == esperado.nome, f"O nome do administrador {i} obtido não corresponde ao esperado."
            assert administrador.cpf == esperado.cpf, f"O CPF do administrador {i} obtido não corresponde ao esperado."
            assert administrador.email == esperado.email, f"O email do administrador {i} obtido não corresponde ao esperado."
            assert administrador.senha == esperado.senha, f"A senha do administrador {i} obtido não corresponde à esperada."
            assert administrador.genero == esperado.genero, f"O gênero do administrador {i} obtido não corresponde ao esperado."
            assert administrador.dataNascimento == esperado.dataNascimento, f"A data de nascimento do administrador {i} obtido não corresponde ao esperado."
           
    def test_obter_administrador_por_id(self, test_db, administrador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        id_adm_inserido = inserir_administrador(administrador_exemplo)
        administrador_exemplo.idUsuario = id_adm_inserido
        administrador_exemplo.idAdministrador = id_adm_inserido
        # Act
        administrador_obtido = obter_administrador_por_id(id_adm_inserido)
        # Assert
        assert administrador_obtido is not None, "O administrador obtido não deve ser None."
        assert administrador_obtido.idAdministrador == id_adm_inserido, "O ID do administrador obtido não corresponde ao ID inserido."
        assert administrador_obtido.idUsuario == id_adm_inserido, "O ID do usuário do administrador obtido não corresponde ao ID inserido."
        assert administrador_obtido.nome == administrador_exemplo.nome, "O nome do administrador obtido não corresponde ao esperado."
        assert administrador_obtido.cpf == administrador_exemplo.cpf, "O CPF do administrador obtido não corresponde ao esperado."
        assert administrador_obtido.email == administrador_exemplo.email, "O email do administrador obtido não corresponde ao esperado."
        assert administrador_obtido.senha == administrador_exemplo.senha, "A senha do administrador obtido não corresponde ao esperado."
        assert administrador_obtido.genero == administrador_exemplo.genero, "O gênero do administrador obtido não corresponde ao esperado."
        assert administrador_obtido.dataNascimento == administrador_exemplo.dataNascimento, "A data de nascimento do administrador obtido não corresponde ao esperado."

    def test_obter_administradores_por_pagina(self, test_db, lista_administradores_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        for i, administrador in enumerate(lista_administradores_exemplo):
            id_inserido = inserir_administrador(administrador)
            administrador.idUsuario = id_inserido
            administrador.idAdministrador = id_inserido
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        administradores = obter_administradores_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(administradores) == tamanho_pagina, "O número de administradores obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, administrador in enumerate(administradores):
            esperado = lista_administradores_exemplo[start_index + i]
            assert administrador.idAdministrador == esperado.idAdministrador, f"O ID do administrador {i} obtido não corresponde ao esperado."
            assert administrador.idUsuario == esperado.idUsuario, f"O ID do usuário do administrador {i} obtido não corresponde ao esperado."
            assert administrador.nome == esperado.nome, f"O nome do administrador {i} obtido não corresponde ao esperado."
            assert administrador.cpf == esperado.cpf, f"O CPF do administrador {i} obtido não corresponde ao esperado."
            assert administrador.email == esperado.email, f"O email do administrador {i} obtido não corresponde ao esperado."
            assert administrador.senha == esperado.senha, f"A senha do administrador {i} obtido não corresponde à esperada."
            assert administrador.genero == esperado.genero, f"O gênero do administrador {i} obtido não corresponde ao esperado."
            assert administrador.dataNascimento == esperado.dataNascimento, f"A data de nascimento do administrador {i} obtido não corresponde à esperada."

    def test_atualizar_administrador(self, test_db, administrador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        id_adm_inserido = inserir_administrador(administrador_exemplo)
        administrador_exemplo.idUsuario = id_adm_inserido
        administrador_exemplo.idAdministrador = id_adm_inserido
        administrador_exemplo.nome = "admin_atualizado"
        administrador_exemplo.cpf = "22233344455"
        administrador_exemplo.email = "atualizado"
        administrador_exemplo.genero = "Feminino"
        administrador_exemplo.dataNascimento = "1990-01-01"
        # Act
        resultado = atualizar_administrador(administrador_exemplo)
        # Assert
        assert resultado == True, "A atualização do administrador falhou."
        administrador_atualizado = obter_administrador_por_id(id_adm_inserido)
        assert administrador_atualizado is not None, "O administrador atualizado não foi encontrado."
        assert administrador_atualizado.idAdministrador == id_adm_inserido, "O ID do administrador atualizado não corresponde ao ID inserido."
        assert administrador_atualizado.idUsuario == id_adm_inserido, "O ID do usuário do administrador atualizado não corresponde ao ID inserido."
        assert administrador_atualizado.nome == "admin_atualizado", "O nome do administrador atualizado não corresponde ao esperado."
        assert administrador_atualizado.cpf == "22233344455", "O CPF do administrador atualizado não corresponde ao esperado."
        assert administrador_atualizado.email == "atualizado", "O email do administrador atualizado não corresponde ao esperado."
        assert administrador_atualizado.genero == "Feminino", "O gênero do administrador atualizado não corresponde ao esperado."
        assert administrador_atualizado.dataNascimento == "1990-01-01", "A data de nascimento do administrador atualizado não corresponde ao esperado."

    def test_atualizar_senha_administrador(self, test_db, administrador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        id_adm_inserido = inserir_administrador(administrador_exemplo)
        nova_senha = "nova_senha123"
        # Act
        resultado = atualizar_senha_administrador(id_adm_inserido, nova_senha)
        # Assert
        assert resultado == True, "A atualização da senha do administrador falhou."
        usuario_atualizado = obter_usuario_por_id(id_adm_inserido)
        assert usuario_atualizado is not None, "O usuário do administrador atualizado não foi encontrado."
        assert usuario_atualizado.senha == nova_senha, "A senha do usuário do administrador atualizado não corresponde à nova senha."

    def test_atualizar_senha_administrador_inexistente(self, test_db, usuario_exemplo): #na verdade testa se eu consigo atualizar um usuario que existe, mas que não é paciente
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        id_adm_inexistente = id_usuario_inserido
        nova_senha = "novaSenha123"
        # Act
        resultado = atualizar_senha_administrador(id_adm_inexistente, nova_senha)
        # Assert
        assert resultado == False, "A atualização da senha do adm inexistente não deve ser bem-sucedida."

    def test_deletar_administrador(self, test_db, administrador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        id_administrador = inserir_administrador(administrador_exemplo)
        # Act
        resultado = deletar_administrador(id_administrador)
        # Assert
        assert resultado == True, "A deleção do administrador falhou."
        administrador_obtido = obter_administrador_por_id(id_administrador)
        assert administrador_obtido is None, "O administrador obtido não deve existir após a deleção."
        usuario_obtido = obter_usuario_por_id(id_administrador)
        assert usuario_obtido is None, "O usuário do administrador obtido não deve existir após a deleção."



       
    
           

