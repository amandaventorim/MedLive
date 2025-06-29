import sys
import os

from data.repo import paciente_repo, usuario_repo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *

class TestPacienteRepo:
    def test_criar_tabela_paciente(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_paciente()
        # Assert
        assert resultado == True, "A criação da tabela 'paciente' falhou."

    def test_obter_paciente_por_primeira_pagina(self, test_db, lista_pacientes_exemplo, lista_usuarios_exemplo):
        # Arrange
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_pacientes = paciente_repo.obter_pacientes_por_pagina(1, 4)
        # Assert
        assert len(pagina_pacientes) == 4, "Deve retornar 4 pacientes na primeira página."
        nomes_esperados = ["Paciente 01", "Paciente 02", "Paciente 03", "Paciente 04"]
        nomes_recebidos = [paciente.nome for paciente in pagina_pacientes]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos pacientes na primeira página não correspondem aos esperados."

    def test_obter_paciente_por_terceira_pagina(self, test_db, lista_pacientes_exemplo, lista_usuarios_exemplo):
        # Arrange
        paciente_repo.criar_tabela_paciente()
        for paciente in lista_pacientes_exemplo():
            paciente_repo.inserir_paciente(paciente)
        usuario_repo.criar_tabela_usuario()
        for usuario in lista_usuarios_exemplo():
            usuario_repo.inserir_usuario(usuario)
        # Act
        pagina_pacientes = paciente_repo.obter_pacientes_por_pagina(3, 4)
        # Assert
        assert len(pagina_pacientes) == 2, "Deve retornar 2 pacientes na terceira página."
        nomes_esperados = ["Paciente 09", "Paciente 10"]
        nomes_recebidos = [paciente.nome for paciente in pagina_pacientes]
        assert nomes_recebidos == nomes_esperados, "Os nomes dos pacientes na terceira página não correspondem aos esperados."
    
    def test_obter_paciente_por_pagina_vazia(self, test_db):
        # Arrange
        paciente_repo.criar_tabela_paciente()
        usuario_repo.criar_tabela_usuario()
        # Act
        pagina_pacientes = paciente_repo.obter_pacientes_por_pagina(1, 10)
        # Assert
        assert isinstance(pagina_pacientes, list), "A página de pacientes deve ser uma lista."
        assert len(pagina_pacientes) == 0, "A página de pacientes não deve conter resultados quando a tabela está vazia."