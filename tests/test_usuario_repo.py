import sys
import os
from data.model.usuario_model import Usuario
from data.repo import usuario_repo
from data.repo.usuario_repo import *

class TestUsuarioRepo:
    def test_criar_tabela_medicamento(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_usuario()
        # Assert
        assert resultado == True, "A criação da tabela 'medicamento' falhou."

    def test_obter_usuario_por_primeira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_usuarios = usuario_repo.obter_usuarios_por_pagina(1, 4)
        # Assert
        assert len(pagina_usuarios) == 4, "Deve retornar 4 usuários na primeira página."
        ids_esperados = [1, 2, 3, 4]
        ids_recebidos = [usuario.idUsuario for usuario in pagina_usuarios]
        assert ids_recebidos == ids_esperados, "Os IDs dos usuários na primeira página não correspondem aos esperados."
        
    def test_obter_usuario_por_terceira_pagina(self, test_db, lista_usuarios_exemplo):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_usuarios = usuario_repo.obter_usuarios_por_pagina(3, 4)
        # Assert
        assert len(pagina_usuarios) == 2, "Deve retornar 2 usuários na terceira página."
        ids_esperados = [9, 10]
        ids_recebidos = [usuario.idUsuario for usuario in pagina_usuarios]
        assert ids_recebidos == ids_esperados, "Os IDs dos usuários na terceira página não correspondem aos esperados."

    def test_obter_usuario_por_pagina_vazia(self, test_db):
        # Arrange
        usuario_repo.criar_tabela_usuario()
        # Act
        pagina_usuarios = usuario_repo.obter_usuarios_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_usuarios, list), "A página de usuários deve ser uma lista."
        assert len(pagina_usuarios) == 0, "A página de usuários não deve conter resultados quando a tabela está vazia."


