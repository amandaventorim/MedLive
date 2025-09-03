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
        usuario_teste = Usuario(
            idUsuario=0,
            nome="João Silva",
            cpf="12345678901",
            email="joao@gmail.com",
            senha="senha123",
            genero="Masculino",
            dataNascimento="1990-01-01",
            perfil="paciente",
            foto="foto.jpg",
            token_redefinicao="token123",
            data_token="2025-09-03 10:00:00",
            data_cadastro="2025-09-03 09:00:00"
        )
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
        assert usuario_db.perfil == "paciente", "O perfil do usuário inserido deve ser igual ao perfil inserido"
        assert usuario_db.foto == "foto.jpg", "A foto do usuário inserido deve ser igual à foto inserida"
        assert usuario_db.token_redefinicao == "token123", "O token de redefinição deve ser igual ao inserido"
        assert usuario_db.data_token == "2025-09-03 10:00:00", "A data do token deve ser igual à inserida"
        assert usuario_db.data_cadastro == "2025-09-03 09:00:00", "A data de cadastro deve ser igual à inserida"

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
        usuario_inserido.perfil = "admin"
        usuario_inserido.foto = "foto2.jpg"
        usuario_inserido.token_redefinicao = "token456"
        usuario_inserido.data_token = "2025-09-03 11:00:00"
        usuario_inserido.data_cadastro = "2025-09-03 10:00:00"
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
        assert usuario_db.perfil == "admin", "O perfil do usuário não foi alterado corretamente."
        assert usuario_db.foto == "foto2.jpg", "A foto do usuário não foi alterada corretamente."
        assert usuario_db.token_redefinicao == "token456", "O token de redefinição não foi alterado corretamente."
        assert usuario_db.data_token == "2025-09-03 11:00:00", "A data do token não foi alterada corretamente."
        assert usuario_db.data_cadastro == "2025-09-03 10:00:00", "A data de cadastro não foi alterada corretamente."

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

    def test_obter_usuarios_por_perfil(self, test_db, usuario_exemplo):
    # Arrange
    criar_tabela_usuario()
    id_usuario_inserido = inserir_usuario(usuario_exemplo)
    # Act
    usuarios_db = obter_todos_por_perfil("paciente")
    # Assert
    assert len(usuarios_db) > 0, "Nenhum usuário foi encontrado com o perfil 'paciente'."
    usuario_db = usuarios_db[0]
    assert usuario_db.idUsuario == id_usuario_inserido, "O ID do usuário obtido não corresponde ao ID inserido."
    assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuário obtido não corresponde ao nome inserido."
    assert usuario_db.cpf == usuario_exemplo.cpf, "O CPF do usuário obtido não corresponde ao CPF inserido."
    assert usuario_db.email == usuario_exemplo.email, "O email do usuário obtido não corresponde ao email inserido."
    assert usuario_db.senha == usuario_exemplo.senha, "A senha do usuário obtido não corresponde à senha inserida."
    assert usuario_db.genero == usuario_exemplo.genero, "O gênero do usuário obtido não corresponde ao gênero inserido."
    assert usuario_db.dataNascimento == usuario_exemplo.dataNascimento, "A data de nascimento do usuário obtido não corresponde à data de nascimento inserida."
    assert usuario_db.perfil == usuario_exemplo.perfil, "O perfil do usuário obtido não corresponde ao perfil inserido."
    assert usuario_db.foto == usuario_exemplo.foto, "A foto do usuário obtido não corresponde à foto inserida."
    assert usuario_db.token_redefinicao == usuario_exemplo.token_redefinicao, "O token de redefinição do usuário obtido não corresponde ao inserido."
    assert usuario_db.data_token == usuario_exemplo.data_token, "A data do token do usuário obtido não corresponde à inserida."
    assert usuario_db.data_cadastro == usuario_exemplo.data_cadastro, "A data de cadastro do usuário obtido não corresponde à inserida."

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

                         
