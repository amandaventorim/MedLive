import sys
import os
from data.model.administrador_model import Administrador
from data.repo.administrador_repo import *

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_administrador()
        # Assert
        assert resultado == True, "A criação da tabela 'administrador' falhou."

    def test_obter_administradores_por_primeira_pagina(self, test_db, lista_administradores_exemplo):
        # Arrange
        criar_tabela_administrador()
        for i in range(10):
            admin_teste = Administrador(0, f"Admin {i + 1}")
            inserir_administrador(admin_teste)
        # Act
        admins1 = obter_administradores_por_pagina(1, 10)
        admins2 = obter_administradores_por_pagina(2, 4)
        admins3 = obter_administradores_por_pagina(3, 4)
        # Assert
        assert len(admins1) == 10, "Deve retornar 10 administradores na primeira página."
        assert len(admins2) == 4, "Deve retornar 4 administradores na segunda página."
        assert len(admins3) == 2, "Deve retornar 2 administradores na terceira página."
        assert admins3[0].idAdministrador == 9, "O primeiro administrador da terceira página deve ter ID 9."