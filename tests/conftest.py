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
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    # Configura a variável de ambiente para usar o banco de teste
    os.environ["TEST_DATABASE_PATH"] = db_path
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
def medico_exemplo():
    from data.model.medico_model import Medico
    medico = Medico(0, "medico_teste", "123456789{i:02}", "medicoteste@email.com", "senha123", "Feminino", "2000-01-01", 0, "CRM123", "Ativo")
    return medico

@pytest.fixture
def lista_medicos_exemplo():
    # Cria uma lista de 10 médicos de exemplo
    from data.model.medico_model import Medico
    medicos = []
    for i in range(1, 11):
        medico = Medico(0, "medico_teste", "123456789{i:02}", "medicoteste@email.com", "senha123", "Feminino", "2000-01-01", i, f"CRM-{i:03d}", "Ativo")
        medicos.append(medico)
    return medicos

@pytest.fixture
def paciente_exemplo():
    from data.model.paciente_model import Paciente
    paciente = Paciente(0, "paciente_teste", "12345678900", "pacienteteste@email.com", "senha123", "Masculino", "2000-01-01", 0, "Rua Exemplo, 123", "Convênio Exemplo")
    return paciente

@pytest.fixture
def lista_pacientes_exemplo():
    # Cria uma lista de 10 pacientes de exemplo
    from data.model.paciente_model import Paciente
    pacientes = []
    for i in range(1, 11):
        paciente = Paciente(0, "paciente_teste", "12345678900", "pacienteteste@email.com", "senha123", "Masculino", "2000-01-01", i, f"Rua Exemplo {i:02d}, 123", f"Convênio {i:02d}")
        pacientes.append(paciente)
    return pacientes

@pytest.fixture
def usuario_exemplo():
    from data.model.usuario_model import Usuario
    usuario = Usuario(
        idUsuario=0,
        nome="usuario_teste",
        cpf="12345678900",
        email="usuarioteste@email.com",
        senha="senha123",
        genero="Masculino",
        dataNascimento="2000-01-01",
        perfil="paciente",
        foto="foto_teste.jpg",
        token_redefinicao="token_teste",
        data_token="2025-09-03 12:00:00",
        data_cadastro="2025-09-03 11:00:00"
    )
    return usuario

@pytest.fixture
def lista_usuarios_exemplo():
    # Cria uma lista de 10 usuários de exemplo
    from data.model.usuario_model import Usuario
    usuarios = []
    for i in range(1, 11):
        usuario = Usuario(i, f"Usuário {i:02d}", f"{i:011d}", f"usuarioteste{i:02d}@email.com", "senha123", "Masculino", "2000-01-01")
        usuarios.append(usuario)
    return usuarios

@pytest.fixture
def item_receita_exemplo():
    from data.model.item_receita_model import ItemReceita
    item = ItemReceita(0, 0, "Descrição do item de receita")
    return item

@pytest.fixture
def especialidade_exemplo():
    from data.model.especialidade_model import Especialidade
    especialidade = Especialidade(0, "Especialidade Exemplo", "Descrição da especialidade exemplo")
    return especialidade

@pytest.fixture
def lista_especialidades_exemplo():
    # Cria uma lista de 10 especialidades de exemplo
    from data.model.especialidade_model import Especialidade
    especialidades = []
    for i in range(1, 11):
        especialidade = Especialidade(i, f"Especialidade {i:02d}", "Descrição da especialidade")
        especialidades.append(especialidade)
    return especialidades

@pytest.fixture
def entrada_prontuario_exemplo():
    from data.model.entrada_prontuario_model import EntradaProntuario
    entrada = EntradaProntuario(idProntuario=0, data="2023-01-01", queixaPrincipal="Queixa principal exemplo", alergias="Alergias exemplo", solicitacoesExames="Solicitações de exames exemplo", antecedentesFamiliares="Antecedentes familiares exemplo", fatoresAlivio="Fatores de alívio exemplo", fatoresPiora="Fatores de piora exemplo", fatoresPredecessores="Fatores predecessores exemplo", idConsulta=0)
    return entrada

@pytest.fixture
def consulta_exemplo():
    from data.model.consulta_model import Consulta
    consulta = Consulta(idConsulta=0, idMedico=0, idPaciente=0, dataHora="2023-01-01", queixa="Motivo da consulta exemplo", conduta="Observações da consulta exemplo")
    return consulta

@pytest.fixture
def agendamento_exemplo():
    from data.model.agendamento_model import Agendamento
    agendamento = Agendamento(
        idAgendamento=0,
        idPaciente=0,
        idMedico=0,
        dataAgendamento="2023-01-01",
        horario="09:00",
        status="agendado",
        queixa="Consulta de rotina",
        preco=150.0
    )
    return agendamento

@pytest.fixture
def agenda_exemplo():
    from data.model.agenda_model import Agenda
    agenda = Agenda(0, 0, "2023-01-01", True)
    return agenda

@pytest.fixture
def administrador_exemplo():
    from data.model.administrador_model import Administrador
    administrador = Administrador(0, "admin_teste", "11122233344", "admin@email.com", "admin123", "Masculino", "2000-01-01", 0)
    return administrador

@pytest.fixture
def lista_administradores_exemplo():
    # Cria uma lista de 10 administradores de exemplo
    from data.model.administrador_model import Administrador
    administradores = []
    for i in range(1, 11):
        administrador = Administrador(i, f"admin_teste_{i:02d}", f"111222333{i:02d}", f"admin{i:01}email.com", "admin123", "Masculino", "2000-01-01", i)
        administradores.append(administrador)
    return administradores    




@pytest.fixture
def lista_consultas_exemplo():
    from data.model.consulta_model import Consulta
    consultas = []
    for i in range(1, 11):
        consulta = Consulta(idConsulta=i, idMedico=0, idPaciente=0, dataHora=f"2023-01-{i:02d}", queixa=f"Queixa {i}", conduta=f"Conduta {i}")
        consultas.append(consulta)
    return consultas




@pytest.fixture
def lista_itens_receita_exemplo():
    from data.model.item_receita_model import ItemReceita
    itens = []
    for i in range(1, 11):
        item = ItemReceita(idConsulta=0, idMedicamento=0, descricao=f"Descrição do item {i}")
        itens.append(item)
    return itens




@pytest.fixture
def lista_medicos_especialidades_exemplo():
    from data.model.medico_especialidade_model import MedicoEspecialidade
    medicos_especialidades = []
    for i in range(1, 11):
        medico_especialidade = MedicoEspecialidade(idMedico=0, idEspecialidade=0, dataHabilitacao=f"2023-01-{i:02d}")
        medicos_especialidades.append(medico_especialidade)
    return medicos_especialidades


