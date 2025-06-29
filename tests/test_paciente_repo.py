import sys
import os
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

    def test_obter_paciente_por_pagina(self, test_db):
        # Arrange
        criar_tabela_paciente()
        for i in range(10):
            paciente_teste = Paciente(0, f"Rua Exemplo {i + 1}, 123", f"Convênio {i + 1}")
            inserir_paciente(paciente_teste)
        # Act
        pacientes1 = obter_pacientes_por_pagina(1, 10)
        pacientes2 = obter_pacientes_por_pagina(2, 4)
        pacientes3 = obter_pacientes_por_pagina(3, 4)
        # Assert
        assert len(pacientes1) == 10, "Deve retornar 10 pacientes na primeira página."
        assert len(pacientes2) == 4, "Deve retornar 4 pacientes na segunda página."
        assert len(pacientes3) == 2, "Deve retornar 2 pacientes na terceira página."
        assert pacientes3[0].idPaciente == 9, "O primeiro paciente da terceira página deve ter ID 9."