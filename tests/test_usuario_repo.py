import sys
import os
from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *

class TestUsuarioRepo:
    def test_criar_tabela_medicamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_usuario()
        # Assert
        assert resultado == True, "A criação da tabela 'medicamento' falhou."

    def test_obter_usuario_por_pagina(self, test_db):
        # Arrange
        criar_tabela_usuario()
        for i in range(10):
            usuario_teste = Usuario(0, f"Usuario {i + 1}", f"cpf{i + 1}", f"usuarioteste{i + 1}@email.com", "senha123", "Masculino", "2000-01-01")
            inserir_usuario(usuario_teste)
        # Act
        usuarios1 = obter_usuarios_por_pagina(1, 10)
        usuarios2 = obter_usuarios_por_pagina(2, 4)
        usuarios3 = obter_usuarios_por_pagina(3, 4)
        # Assert
        assert len(usuarios1) == 10, "Deve retornar 10 usuários na primeira página."
        assert len(usuarios2) == 4, "Deve retornar 4 usuários na segunda página."
        assert len(usuarios3) == 2, "Deve retornar 2 usuários na terceira página."
        assert usuarios3[0].idUsuario == 9, "O primeiro usuário da terceira página deve ter ID 9."



