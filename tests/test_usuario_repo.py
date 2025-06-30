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

    def test_atualizar_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0, "João Silva", "12345678901", "joao@gmail.com", "senha123", "Masculino", "1990-01-01")
        id_usuario_inserido = inserir_usuario(usuario_teste)
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
        # Act
        nova_senha = "novaSenha123" 
        resultado = atualizar_senha_usuario(id_usuario_inserido, nova_senha)
        # Assert
        assert resultado == True, "A atualização da senha do usuário falhou."
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuário não foi encontrado no banco de dados."
        assert usuario_db.senha == nova_senha, "A senha do usuário não foi atualizada corretamente."

    def test_obter_todos_usuarios(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste1 = Usuario(0, "João Silva", "12345678901", "joao@gmail.com", "senha123", "Masculino", "1990-01-01")
        usuario_teste2 = Usuario(0, "Maria Souza", "10987654321", "maria@gmail.com", "senha456", "Feminino", "1992-02-02") 
        inserir_usuario(usuario_teste1)
        inserir_usuario(usuario_teste2)
        # Act
        usuarios = obter_todos_usuarios()
        # Assert
        assert len(usuarios) == 2, "O número de usuários obtidos não é igual a 2."
        assert usuarios[0].idUsuario == 1, "O ID do primeiro usuário não é o esperado."
        assert usuarios[1].idUsuario == 2, "O ID do segundo usuário não é o esperado."
        assert usuarios[0].nome == "João Silva", "O primeiro usuário não é o esperado."
        assert usuarios[1].nome == "Maria Souza", "O segundo usuário não é o esperado." 
        assert usuarios[0].cpf == "12345678901", "O CPF do primeiro usuário não é o esperado."
        assert usuarios[1].cpf == "10987654321", "O CPF do segundo usuário não é o esperado."
        assert usuarios[0].email == "joao@gmail.com", "O email do primeiro usuário não é o esperado."
        assert usuarios[1].email == "maria@gmail.com", "O email do segundo usuário não é o esperado."
        assert usuarios[0].senha == "senha123", "A senha do segundo usuário não é o esperado."
        assert usuarios[1].senha == "senha456", "A senha do segundo usuário não é o esperado."
        assert usuarios[0].genero == "Masculino", "O gênero do primeiro usuário não é o esperado."
        assert usuarios[1].genero == "Feminino", "O gênero do segundo usuário não é o esperado."    

    def test_obter_usuarios_por_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo:
            inserir_usuario(usuario)
        numero_pagina = 2
        tamanho_pagina = 5
        # Act
        usuarios = obter_usuarios_por_pagina(numero_pagina, tamanho_pagina)
        # Assert
        assert len(usuarios) == tamanho_pagina, "O número de usuários obtidos por página não corresponde ao tamanho da página."
        start_index = (numero_pagina - 1) * tamanho_pagina
        for i, usuario in enumerate(usuarios):
            esperado = lista_usuarios_exemplo[start_index + i]
            assert usuario.idUsuario == esperado.idUsuario, f"O ID do usuário {i} obtido não corresponde ao esperado."
            assert usuario.nome == esperado.nome, f"O nome do usuário {i} obtido não corresponde ao esperado."
            assert usuario.cpf == esperado.cpf, f"O CPF do usuário {i} obtido não corresponde ao esperado."
            assert usuario.email == esperado.email, f"O email do usuário {i} obtido não corresponde ao esperado."
            assert usuario.senha == esperado.senha, f"A senha do usuário {i} obtido não corresponde à esperada."
            assert usuario.genero == esperado.genero, f"O gênero do usuário {i} obtido não corresponde ao esperado."
            assert usuario.dataNascimento == esperado.dataNascimento, f"A data de nascimento do usuário {i} obtido não corresponde à esperada."

    def test_obter_usuario_por_id(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        # Act
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        # Assert
        assert usuario_db is not None, "O usuário não foi encontrado no banco de dados."    
        assert usuario_db.idUsuario == id_usuario_inserido, "O ID do usuário obtido não é o esperado."
        assert usuario_db.nome == usuario_exemplo.nome, "O nome do usuário obtido não é o esperado."
        assert usuario_db.cpf == usuario_exemplo.cpf, "O CPF do usuário obtido não é o esperado."
        assert usuario_db.email == usuario_exemplo.email, "O email do usuário obtido não é o esperado."
        assert usuario_db.senha == usuario_exemplo.senha, "A senha do usuário obtido não é o esperado."
        assert usuario_db.genero == usuario_exemplo.genero, "O gênero do usuário obt  ido não é o esperado."
        assert usuario_db.dataNascimento == usuario_exemplo.dataNascimento, "A data de nascimento do  usuário obtido não é o esperado"   

    def test_deletar_usuario(self, test_db, usuario_exemplo):
        # Arrange
        criar_tabela_usuario()
        id_usuario_inserido = inserir_usuario(usuario_exemplo)
        # Act
        resultado = deletar_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "A exclusão do usuário falhou."
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db == None, "O usuário ainda existe no banco de dados após a exclusão."

