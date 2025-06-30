import os
import sys
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *
from data.repo.usuario_repo import criar_tabela_usuario, inserir_usuario, obter_usuario_por_id
from tests.conftest import usuario_exemplo


class TestPacienteRepo:
    def test_criar_tabela_paciente(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_paciente()
        # Assert
        assert resultado == True, "A criação da tabela 'paciente' falhou."

    def test_inserir_paciente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        paciente_teste = Paciente(0, "paciente_teste", "12345678900", "pacienteteste@email.com", "senha123", "Masculino", "2000-01-01", 0, "Rua Exemplo, 123", "Convênio Exemplo")
        # Act
        id_paciente_inserido = inserir_paciente(paciente_teste)
        # Assert
        paciente_db = obter_paciente_por_id(id_paciente_inserido)
        assert paciente_db is not None, "O paciente inserido não foi encontrado na tabela paciente do banco de dados."
        usuario_db = obter_usuario_por_id(paciente_db.idUsuario)
        assert usuario_db is not None, "O usuário do paciente inserido não foi encontrado na tabela usuario do banco de dados."
        assert paciente_db.idPaciente == 1, "O ID do paciente inserido deve ser igual a 1"
        assert paciente_db.idUsuario == 1, "O ID do usuário do paciente inserido deve ser igual a 1"
        assert usuario_db.nome == "paciente_teste", "O nome do paciente inserido deve ser igual ao nome inserido"
        assert usuario_db.cpf == "12345678900", "O CPF do paciente inserido deve ser igual ao CPF inserido"
        assert usuario_db.email == "pacienteteste@email.com", "O email do paciente inserido deve ser igual ao email inserido"
        assert usuario_db.senha == "senha123", "A senha do paciente inserido deve ser igual à senha inserida"
        assert usuario_db.genero == "Masculino", "O gênero do paciente inserido deve ser igual ao gênero inserido"
        assert usuario_db.dataNascimento == "2000-01-01", "A data de nascimento do paciente inserido deve ser igual à data de nascimento inserida"  
        assert paciente_db.endereco == "Rua Exemplo, 123", "O endereço do paciente inserido deve ser igual ao endereço inserido"
        assert paciente_db.convenio == "Convênio Exemplo", "O convênio do paciente inserido deve ser igual ao convênio inserido"

    def test_obter_todos_pacientes(self, test_db, lista_pacientes_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        for i, paciente in enumerate(lista_pacientes_exemplo):
            id_inserido = inserir_paciente(paciente)
            paciente.idUsuario = id_inserido
            paciente.idPaciente = id_inserido 
        # Act
        pacientes = obter_todos_pacientes()
        # Assert
        assert len(pacientes) == len(lista_pacientes_exemplo), "O número de pacientes obtidos não corresponde ao número de pacientes inseridos."
        for i, paciente in enumerate(pacientes):
            assert paciente.idPaciente == lista_pacientes_exemplo[i].idPaciente, f"O ID do paciente {i} obtido não corresponde ao ID do paciente inserido."
            assert paciente.idUsuario == lista_pacientes_exemplo[i].idUsuario, f"O ID do usuário do paciente {i} obtido não corresponde ao ID do usuário do paciente inserido."
            assert paciente.nome == lista_pacientes_exemplo[i].nome, f"O nome do paciente {i} obtido não corresponde ao nome do paciente inserido."
            assert paciente.cpf == lista_pacientes_exemplo[i].cpf, f"O CPF do paciente {i} obtido não corresponde ao CPF do paciente inserido."
            assert paciente.email == lista_pacientes_exemplo[i].email, f"O email do paciente {i} obtido não corresponde ao email do paciente inserido."
            assert paciente.senha == lista_pacientes_exemplo[i].senha, f"A senha do paciente {i} obtido não corresponde à senha do paciente inserido."
            assert paciente.genero == lista_pacientes_exemplo[i].genero, f"O gênero do paciente {i} obtido não corresponde ao gênero do paciente inserido."
            assert paciente.dataNascimento == lista_pacientes_exemplo[i].dataNascimento, f"A data de nascimento do paciente {i} obtido não corresponde à data de nascimento do paciente inserido."
            assert paciente.endereco == lista_pacientes_exemplo[i].endereco, f"O endereço do paciente {i} obtido não corresponde ao endereço do paciente inserido."
            assert paciente.convenio == lista_pacientes_exemplo[i].convenio, f"O convênio do paciente {i} obtido não corresponde ao convênio do paciente inserido."

    def test_obter_pacientes_por_pagina(self, test_db, lista_pacientes_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        for i, paciente in enumerate(lista_pacientes_exemplo):
            id_inserido = inserir_paciente(paciente)
            paciente.idUsuario = id_inserido
            paciente.idPaciente = id_inserido
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        pacientes = obter_pacientes_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(pacientes) == tamanho_pagina, "O número de pacientes obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, paciente in enumerate(pacientes):
            esperado = lista_pacientes_exemplo[start_index + i]
            assert paciente.idPaciente == esperado.idPaciente, f"O ID do paciente {i} obtido não corresponde ao ID do paciente inserido."
            assert paciente.idUsuario == esperado.idUsuario, f"O ID do usuário do paciente {i} obtido não corresponde ao ID do usuário do paciente inserido."
            assert paciente.nome == esperado.nome, f"O nome do paciente {i} obtido não corresponde ao nome do paciente inserido."
            assert paciente.cpf == esperado.cpf, f"O CPF do paciente {i} obtido não corresponde ao CPF do paciente inserido."
            assert paciente.email == esperado.email, f"O email do paciente {i} obtido não corresponde ao email do paciente inserido."
            assert paciente.senha == esperado.senha, f"A senha do paciente {i} obtido não corresponde à senha do paciente inserido."
            assert paciente.genero == esperado.genero, f"O gênero do paciente {i} obtido não corresponde ao gênero do paciente inserido."
            assert paciente.dataNascimento == esperado.dataNascimento, f"A data de nascimento do paciente {i} obtido não corresponde à data de nascimento do paciente inserido."
            assert paciente.endereco == esperado.endereco, f"O endereço do paciente {i} obtido não corresponde ao endereço do paciente inserido."
            assert paciente.convenio == esperado.convenio, f"O convênio do paciente {i} obtido não corresponde ao convênio do paciente inserido."
       

    def test_obter_paciente_por_id(self, test_db, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_paciente = inserir_paciente(paciente_exemplo)
        # Act
        paciente_obtido = obter_paciente_por_id(id_paciente)
        # Assert
        assert paciente_obtido is not None, "O paciente obtido não deve ser None."
        assert paciente_obtido.idPaciente == id_paciente, "O ID do paciente obtido não corresponde ao ID do paciente inserido."
        assert paciente_obtido.idUsuario == id_paciente, "O ID do usuário do paciente obtido não corresponde ao ID do paciente inserido."
        assert paciente_obtido.nome == paciente_exemplo.nome, "O nome do paciente obtido não corresponde ao nome do paciente inserido."
        assert paciente_obtido.cpf == paciente_exemplo.cpf, "O CPF do paciente obtido não corresponde ao CPF do paciente inserido."
        assert paciente_obtido.email == paciente_exemplo.email, "O email do paciente obtido não corresponde ao email do paciente inserido."
        assert paciente_obtido.senha == paciente_exemplo.senha, "A senha do paciente obtido não corresponde à senha do paciente inserido."
        assert paciente_obtido.genero == paciente_exemplo.genero, "O gênero do paciente obtido não corresponde ao gênero do paciente inserido."
        assert paciente_obtido.dataNascimento == paciente_exemplo.dataNascimento, "A data de nascimento do paciente obtido não corresponde à data de nascimento do paciente inserido."
        assert paciente_obtido.endereco == paciente_exemplo.endereco, "O endereço do paciente obtido não corresponde ao endereço do paciente inserido."
        assert paciente_obtido.convenio == paciente_exemplo.convenio, "O convênio do paciente obtido não corresponde ao convênio do paciente inserido."


    def test_obter_paciente_por_id_inexistente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_inexistente = 9999
        # Act
        paciente_obtido = obter_paciente_por_id(id_inexistente) 
        # Assert
        assert paciente_obtido is None, "O paciente obtido deve ser None quando o ID não existe."


    def test_atualizar_paciente(self, test_db, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_paciente = inserir_paciente(paciente_exemplo)
        paciente_exemplo.idPaciente = id_paciente
        paciente_exemplo.idUsuario = id_paciente
        paciente_exemplo.nome = "Novo Nome"
        paciente_exemplo.cpf = "98765432100"
        paciente_exemplo.email = "novoemail"
        paciente_exemplo.genero = "Feminino"
        paciente_exemplo.dataNascimento = "1990-01-01"
        paciente_exemplo.endereco = "Novo Endereço, 456"
        paciente_exemplo.convenio = "Novo Convênio"
        # Act
        resultado = atualizar_paciente(paciente_exemplo)
        # Assert
        assert resultado == True, "A atualização do paciente falhou."
        usuario_atualizado = obter_usuario_por_id(paciente_exemplo.idUsuario)
        assert usuario_atualizado.nome == "Novo Nome", "O nome do usuário atualizado não corresponde ao novo nome."
        assert usuario_atualizado.cpf == "98765432100", "O CPF do usuário atualizado não corresponde ao novo CPF."
        assert usuario_atualizado.email == "novoemail", "O email do usuário atualizado não corresponde ao novo email."
        assert usuario_atualizado.genero == "Feminino", "O gênero do usuário atualizado não corresponde ao novo gênero."
        assert usuario_atualizado.dataNascimento == "1990-01-01", "A data de nascimento do usuário atualizado não corresponde à nova data de nascimento."
        paciente_atualizado = obter_paciente_por_id(id_paciente)
        assert paciente_atualizado.endereco == "Novo Endereço, 456", "O endereço do paciente atualizado não corresponde ao novo endereço."
        assert paciente_atualizado.convenio == "Novo Convênio", "O convênio do paciente atualizado não corresponde ao novo convênio."

    def test_atualizar_senha_paciente(self, test_db, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_paciente = inserir_paciente(paciente_exemplo)
        nova_senha = "novaSenha123"
        # Act
        resultado = atualizar_senha_paciente(id_paciente, nova_senha)
        # Assert
        assert resultado == True, "A atualização da senha do paciente falhou."
        usuario_atualizado = obter_usuario_por_id(id_paciente)
        assert usuario_atualizado is not None, "O usuário do paciente atualizado não deve ser None."
        assert usuario_atualizado.senha == nova_senha, "A senha do usuário atualizado não corresponde à nova senha."

    def test_atualizar_senha_paciente_inexistente(self, test_db, usuario_exemplo): #na verdade testa se eu consigo atualizar um usuario que existe, mas que não é paciente
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        id_paciente_inexistente = id_usuario_inserido
        nova_senha = "novaSenha123"
        # Act
        resultado = atualizar_senha_paciente(id_paciente_inexistente, nova_senha)
        # Assert
        assert resultado == False, "A atualização da senha do paciente inexistente não deve ser bem-sucedida."

    def test_deletar_paciente(self, test_db, paciente_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_paciente()
        id_paciente = inserir_paciente(paciente_exemplo)
        # Act
        resultado = deletar_paciente(id_paciente)
        # Assert
        assert resultado == True, "A deleção do paciente falhou."
        paciente_obtido = obter_paciente_por_id(id_paciente)
        assert paciente_obtido is None, "O paciente obtido não deve existir após a deleção."
        usuario_obtido = obter_usuario_por_id(id_paciente)
        assert usuario_obtido is None, "O usuário do paciente obtido não deve existir após a deleção."

      
        