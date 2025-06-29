import pytest
import os
import sys
import tempfile



# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def medicamento_exemplo():
    from data.model.medicamento_model import Medicamento
    medicamento = Medicamento(0, "Medicamento teste")
    return medicamento

@pytest.fixture
def lista_medicamentos_exemplo():
    # Cria uma lista de 10 medicamentos de exemplo
    from data.model.medicamento_model import Medicamento
    medicamentos = []
    for i in range(1, 11):
        medicamento = Medicamento(0, f"Medicamento {i:02d}")
        medicamentos.append(medicamento)
    return medicamentos

@pytest.fixture
def medico_especialidade_exemplo():
    from data.model.medico_especialidade_model import MedicoEspecialidade
    medico_especialidade = MedicoEspecialidade(0, 0, "2023-01-01")
    return medico_especialidade

@pytest.fixture
def lista_medico_especialidades_exemplo():
    # Cria uma lista de 10 associações de médicos e especialidades de exemplo
    from data.model.medico_especialidade_model import MedicoEspecialidade
    medico_especialidades = []
    for i in range(1, 11):
        medico_especialidade = MedicoEspecialidade(0, 0, f"2023-01-{i:02d}")
        medico_especialidades.append(medico_especialidade)
    return medico_especialidades

@pytest.fixture
def medico_exemplo():
    from data.model.medico_model import Medico
    medico = Medico(0, "123456", "Ativo")
    return medico

@pytest.fixture
def lista_medicos_exemplo():
    # Cria uma lista de 10 médicos de exemplo
    from data.model.medico_model import Medico
    medicos = []
    for i in range(1, 11):
        medico = Medico(i, f"CRM-{i:03d}", "Ativo")
        medicos.append(medico)
    return medicos

@pytest.fixture
def paciente_exemplo():
    from data.model.paciente_model import Paciente
    paciente = Paciente(0, "Rua Exemplo, 123", "Convênio Exemplo")
    return paciente

@pytest.fixture
def lista_pacientes_exemplo():
    # Cria uma lista de 10 pacientes de exemplo
    from data.model.paciente_model import Paciente
    pacientes = []
    for i in range(1, 11):
        paciente = Paciente(i, f"Rua Exemplo {i:02d}, 123", f"Convênio {i:02d}")
        pacientes.append(paciente)
    return pacientes

def usuario_exemplo():
    from data.model.usuario_model import Usuario
    usuario = Usuario(0, "usuario_teste", "12345678900", "usuarioteste@email.com", "senha123", "Masculino", "2000-01-01")
    return usuario

def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo
    from data.model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(i, f"Usuário {i:02d}", f"{i:011d}", f"usuarioteste{i:02d}@email.com", "senha123", "Masculino", "2000-01-01")
        usuarios.append(usuario)
    return usuarios

def item_receita_exemplo():
    from data.model.item_receita_model import ItemReceita
    item = ItemReceita(0, 0, "Descrição do item de receita")
    return item

def lista_itens_receita_exemplo():
    # Cria uma lista de 10 itens de receita de exemplo
    from data.model.item_receita_model import ItemReceita
    itens = []
    for i in range(1, 11):
        item = ItemReceita(0, 0, f"Descrição do item de receita {i:02d}")
        itens.append(item)
    return itens

def especialidade_exemplo():
    from data.model.especialidade_model import Especialidade
    especialidade = Especialidade(0, "Especialidade Exemplo", "Descrição da especialidade exemplo")
    return especialidade

def lista_especialidades_exemplo():
    # Cria uma lista de 10 especialidades de exemplo
    from data.model.especialidade_model import Especialidade
    especialidades = []
    for i in range(1, 11):
        especialidade = Especialidade(i, f"Especialidade {i:02d}", "Descrição da especialidade")
        especialidades.append(especialidade)
    return especialidades

def entrada_prontuario_exemplo():
    from data.model.entrada_prontuario_model import EntradaProntuario
    entrada = EntradaProntuario(0, 0, "2023-01-01", "Queixa principal exemplo", "Alergias exemplo", "Solicitações de exames exemplo", "Antecedentes familiares exemplo", "Fatores de alívio exemplo", "Fatores de piora exemplo", "Fatores predecessores exemplo")
    return entrada

def lista_entradas_prontuario_exemplo():
    # Cria uma lista de 10 entradas de prontuário de exemplo
    from data.model.entrada_prontuario_model import EntradaProntuario
    entradas = []
    for i in range(1, 11):
        entrada = EntradaProntuario(0, 0, f"2023-01-{i:02d}", "Queixa principal exemplo", "Alergias exemplo", "Solicitações de exames exemplo", "Antecedentes familiares exemplo", "Fatores de alívio exemplo", "Fatores de piora exemplo", "Fatores predecessores exemplo")
        entradas.append(entrada)
    return entradas

def consulta_exemplo():
    from data.model.consulta_model import Consulta
    consulta = Consulta(0, 0, 0, "2023-01-01", "Motivo da consulta exemplo", "Observações da consulta exemplo")
    return consulta

def lista_consultas_exemplo():
    # Cria uma lista de 10 consultas de exemplo
    from data.model.consulta_model import Consulta
    consultas = []
    for i in range(1, 11):
        consulta = Consulta(0, 0, 0, f"2023-01-{i:02d}", f"Motivo da consulta {i:02d}", f"Observações da consulta {i:02d}")
        consultas.append(consulta)
    return consultas

def agendamento_exemplo():
    from data.model.agendamento_model import Agendamento
    agendamento = Agendamento(0, 0, "status exemplo", "2023-01-01")
    return agendamento

def lista_agendamentos_exemplo():
    # Cria uma lista de 10 agendamentos de exemplo
    from data.model.agendamento_model import Agendamento
    agendamentos = []
    for i in range(1, 11):
        agendamento = Agendamento(0, 0, f"status {i:02d}", f"2023-01-{i:02d}")
        agendamentos.append(agendamento)
    return agendamentos

def agenda_exemplo():
    from data.model.agenda_model import Agenda
    agenda = Agenda(0, 0, "2023-01-01", True)
    return agenda

def lista_agendas_exemplo():
    # Cria uma lista de 10 agendas de exemplo
    from data.model.agenda_model import Agenda
    agendas = []
    for i in range(1, 11):
        agenda = Agenda(0, 0, f"2023-01-{i:02d}", True)
        agendas.append(agenda)
    return agendas

def administrador_exemplo():
    from data.model.administrador_model import Administrador
    administrador = Administrador(0)
    return administrador

def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo
    from data.model.administrador_model import Administrador
    administradores = []
    for i in range(1, 11):
        administrador = Administrador(0, f"Administrador {i:02d}")
        administradores.append(administrador)
    return administradores
