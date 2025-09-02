import sys
import os
from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *

class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_usuario()
        # Assert
        assert resultado == True, "A criação da tabela 'usuario' falhou."

    def test_inserir_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0, "João Silva", "12345678901", "joao@gmail.com", "senha123", "Masculino", "1990-01-01")
        # Act
        id_usuario_inserido = inserir_usuario(usuario_teste)    
        # Assert
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuário inserido não foi encontrado no banco de dados."
        assert usuario_db.idUsuario == 1, "O ID do usuário inserido deve ser igual a 1"
        assert usuario_db.nome == "João Silva", "O nome do usuário inserido deve ser igual ao nome inserido"    
        assert usuario_db.cpf == "12345678901", "O CPF do usuário inserido deve ser igual ao CPF inserido"
        assert usuario_db.email == "joao@gmail.com", "O email do usuário inserido deve ser igual ao email inserido"
        assert usuario_db.senha == "senha123", "A senha do usuário inserido deve ser igual à senha inserida"
        assert usuario_db.genero == "Masculino", "O gênero do usuário inserido deve ser igual ao gênero inserido"
        assert usuario_db.dataNascimento == "1990-01-01", "A data de nascimento do usuário inserido deve ser igual à data de nascimento inserida"

    def test_atualizar_usuario(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        usuario_inserido = obter_usuario_por_id(id_usuario_inserido)
        # Act
        usuario_inserido.nome = "João Silva Atualizado"
        usuario_inserido.cpf = "10987654321"
        usuario_inserido.email = "joaoatualizado@gmail.com"
        usuario_inserido.genero = "Masculino Atualizado"
        usuario_inserido.dataNascimento = "1991-01-12" 
        usuario_inserido.idUsuario = id_usuario_inserido
        resultado = atualizar_usuario(usuario_inserido)
        # Assert
        assert resultado == True, "A alteração do usuário falhou."
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "João Silva Atualizado", "O nome do usuário não foi alterado corretamente."
        assert usuario_db.cpf == "10987654321", "O CPF do usuário não foi alterado corretamente."
        assert usuario_db.email == "joaoatualizado@gmail.com", "O email do usuário não foi alterado corretamente."
        assert usuario_db.genero == "Masculino Atualizado", "O gênero do usuário não foi alterado corretamente."
        assert usuario_db.dataNascimento == "1991-01-12", "A data de nascimento do usuário não foi alterada corretamente."

    def test_atualizar_senha_usuario(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        
        nova_senha = "novaSenha123"
        # Act
        resultado = atualizar_senha_usuario(id_usuario_inserido, nova_senha)
        # Assert
        assert resultado == True, "A alteração da senha do usuário falhou."
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.senha == nova_senha, "A senha do usuário não foi alterada corretamente."

    def test_obter_usuario_por_id(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        # Assert
        assert usuario_db is not None, "O usuário não foi encontrado no banco de dados."
        assert usuario_db.idUsuario == id_usuario_inserido, "O ID do usuário obtido não corresponde ao ID inserido."
        assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuário obtido não corresponde ao nome inserido."
        assert usuario_db.cpf == usuario_exemplo.cpf, "O CPF do usuário obtido não corresponde ao CPF inserido."
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário obtido não corresponde ao email inserido."
        assert usuario_db.senha == usuario_exemplo.senha, "A senha do usuário obtido não corresponde à senha inserida."
        assert usuario_db.genero == usuario_exemplo.genero, "O gênero do usuário obtido não corresponde ao gênero inserido."
        assert usuario_db.dataNascimento == usuario_exemplo.dataNascimento, "A data de nascimento do usuário obtido não corresponde à data de nascimento inserida."

    def test_obter_todos_usuarios(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        inserir_usuario(usuario_exemplo)
        # Act
        usuarios_db = obter_todos_usuarios()
        # Assert
        assert len(usuarios_db) > 0, "Nenhum usuário foi encontrado no banco de dados."
        usuario_db = usuarios_db[0]
        assert usuario_db.idUsuario == 1, "O ID do usuário obtido deve ser igual a 1"
        assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuário obtido não corresponde ao nome inserido."
        assert usuario_db.cpf == usuario_exemplo.cpf, "O CPF do usuário obtido não corresponde ao CPF inserido."
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário obtido não corresponde ao email inserido."
        assert usuario_db.senha == usuario_exemplo.senha, "A senha do usuário obtido não corresponde à senha inserida."
        assert usuario_db.genero == usuario_exemplo.genero, "O gênero do usuário obtido não corresponde ao gênero inserido."
        assert usuario_db.dataNascimento == usuario_exemplo.dataNascimento, "A data de nascimento do usuário obtido não corresponde à data de nascimento inserida."

    def test_deletar_usuario(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        # Act
        resultado = deletar_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "A exclusão do usuário falhou."
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is None, "O usuário ainda existe no banco de dados após a exclusão."

                         
