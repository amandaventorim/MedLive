from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *
from data.model.medico_model import Medico
from data.repo.medico_repo import *
from data.model.administrador_model import Administrador
from data.repo.administrador_repo import *
from data.model.especialidade_model import Especialidade
from data.repo.especialidade_repo import *
from data.model.medicamento_model import Medicamento
from data.repo.medicamento_repo import *
from data.model.consulta_model import Consulta
from data.repo.consulta_repo import *
from data.model.entrada_prontuario_model import EntradaProntuario
from data.repo.entrada_prontuario_repo import *
from data.model.medico_especialidade_model import MedicoEspecialidade
from data.repo.medico_especialidade_repo import *
from data.model.item_receita_model import ItemReceita
from data.repo.item_receita_repo import *   
from data.model.agenda_model import Agenda
from data.repo.agenda_repo import *
from data.model.agendamento_model import Agendamento
from data.repo.agendamento_repo import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root():
    response = templates.TemplateResponse("index.html", {"request": {}})
    return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)


# Criar tabelas
criar_tabela_usuario()
criar_tabela_paciente()
criar_tabela_medico()
criar_tabela_administrador()   
criar_tabela_especialidade() 
criar_tabela_medicamento()
criar_tabela_consulta()
criar_tabela_entrada_prontuario()
criar_tabela_medico_especialidade()
criar_tabela_item_receita()
criar_tabela_agenda()
criar_tabela_agendamento()

# print(atualizar_paciente(Paciente(
#     idPaciente=17,  # ID do paciente a ser atualizado
#     idUsuario=17,   # ID do usuário associado
#     nome="osvaldo",
#     cpf="12345678901",
#     email="aaaa",
#     genero="Feminino",
#     senha=0,
#     dataNascimento="1992-03-15",
#     endereco="Rua das Flores, 123",
#     convenio="Unimed"
# )))

# print(atualizar_senha_medico(
#     idMedico=20, 
#     senha="nova"
# ))

# print(atualizar_senha_administrador(
#     idAdministrador=20, 
#     senha="novo"
# ))

# print(inserir_administrador(Administrador(
#     idUsuario=0,
#     idAdministrador= 0,
#     nome="George",
#     cpf="12345678901",
#     email="uuuuuu",
#     senha=0,
#     genero="Masculino",
#     dataNascimento="1985-05-20"
# )))


# print(atualizar_paciente(Paciente(
#     idPaciente=15,  # ID do paciente a ser atualizado
#     idUsuario=15,   # ID do usuário associado
#     nome="Ana Maria",
#     cpf="12345678901",
#     email="aaaa",
#     genero="Feminino",
#     senha=0,
#     dataNascimento="1992-03-15",
#     endereco="Rua das Flores, 123",
#     convenio="Unimed"
# )))

# print(atualizar_medico(Medico(
#     idMedico=20,  # ID do médico a ser atualizado
#     idUsuario=20,  # ID do usuário associado
#     nome="Carlos doroti",
#     cpf="12345678901",
#     email="aaaa",
#     senha=0,
#     genero="Masculino",
#     dataNascimento="1985-05-20",
#     crm="CRM123777",
#     statusProfissional="Ativo"
# )))

# print(atualizar_administrador(Administrador(
#     idUsuario=17,  # ID do usuário a ser atualizado
#     idAdministrador=17,  # ID do administrador associado
#     nome="Carloto",
#     cpf="12345678901",
#     email="oooooo",
#     senha=0,
#     genero="Masculino",
#     dataNascimento="1985-05-20"
# )))

# Inserir usuário (dados comuns)
# usuario = Usuario(
#     idUsuario=0,
#     nome="ana maria clara",
#     cpf="12345678901",
#     email="maria@email.com",
#     senha="senha123",
#     genero="Feminino",
#     dataNascimento="1992-03-15"
# )
# id_usuario = inserir_usuario(usuario)

# Inserir paciente (dados específicos)

# inserir_paciente(paciente = Paciente(
#     idPaciente=id_usuario,
#     idUsuario=id_usuario,  
#     nome=usuario.nome,
#     cpf=usuario.cpf,
#     email=usuario.email,
#     senha=usuario.senha,
#     genero=usuario.genero,
#     dataNascimento=usuario.dataNascimento,
#     endereco="Rua das Flores, 123",
#     convenio="Unimed"))

# Consultar todos os pacientes
# print("🩺 Pacientes no sistema:")
# for p in obter_todos_pacientes():
#     print(p)

# Consultar paciente por ID
# paciente = obter_paciente_por_id(17)
# print(paciente)


# # Verificar atualização
# print("\n✅ Pacientes após atualização:")
# for p in obter_todos_pacientes():
#     print(p)

# paciente = Paciente(
#     idPaciente=0,  # será definido automaticamente
#     idUsuario=0,   # também
#     nome="Geraldo Silva",
#     cpf="11122233344",
#     email="ana@email.com",
#     senha="123456",
#     genero="Feminino",
#     dataNascimento="2000-01-01",
#     endereco="Rua A, 123",
#     convenio="Unimed"
# )
# inserir_usuario_paciente(paciente)

#Atualizar paciente
# print(atualizar_paciente(paciente = Paciente(
#     idPaciente=17,  # ID do paciente a ser atualizado
#     idUsuario=17,   # ID do usuário associado)
#     nome=paciente.nome,
#     cpf=paciente.cpf,
#     email=paciente.email,
#     senha=paciente.senha,
#     genero=paciente.genero,
#     dataNascimento=paciente.dataNascimento,
#     endereco="Rua B, 456",
#     convenio="Bradesco Saúde"
# )))

# deletar_usuario_paciente(19)

# medico = Medico(
#     idMedico=0,  # será gerado automaticamente
#     idUsuario=0,  # igual ao idMedico
#     nome="Guilherme",
#     cpf="44466677788",
#     email="carlos.medico@email.com",
#     senha="med123",
#     genero="Masculino",
#     dataNascimento="1980-06-25",
#     crm="CRM123456",
#     statusProfissional="Ativo"
# )

# id_medico = inserir_usuario_medico(medico)
# print(f"✅ Médico inserido com sucesso! ID: {id_medico}")

# #Consultar todos os médicos
# print("\n🩺 Médicos no sistema:")
# for m in obter_todos_medicos():
#     print(m)

# Consultar médico por ID
# print(obter_medico_por_id(21))

# # Atualizar médico 
# print(atualizar_medico(medico = Medico(
#     idMedico=21,  # ID do médico a ser atualizado
#     idUsuario=21,  # ID do usuário associado
#     nome=medico.nome,
#     cpf=medico.cpf,
#     email=medico.email,
#     senha=medico.senha,
#     genero=medico.genero,
#     dataNascimento=medico.dataNascimento,
#     crm="CRM987654",  # novo CRM
#     statusProfissional="Inativo"  # novo status profissional
# )))

#deletar medico
# print(deletar_usuario_medico(21))


# Criar novo administrador
# administrador = Administrador(
#     idAdministrador=0,  # será gerado automaticamente
#     idUsuario=0,
#     nome="Catarina",
#     cpf="99988877766",
#     email="fernanda.admin@email.com",
#     senha="admin123",
#     genero="Feminino",
#     dataNascimento="1985-10-12"
# )

# # Inserir administrador (usuário + administrador)
# id_admin = inserir_usuario_administrador(administrador)
# print(f"✅ Administrador inserido com sucesso! ID: {id_admin}")

# # Consultar todos os administradores
# print("\n👩‍💼 Administradores no sistema:")
# for a in obter_todos_administradores():
#     print(a)

# Consultar administrador por ID
# print(obter_administrador_por_id(23))


# # Deletar administrador + usuário
# print("\n🗑️ Deletando administrador:")
# print(deletar_usuario_administrador(23))

# Inserir especialidade
# especialidade = Especialidade(
#     idEspecialidade=0,  # será gerado automaticamente
#     nome="Reumatologia",
#     descricao="Especialidade médica que se concentra no diagnóstico e tratamento de doenças reumáticas, como artrite, lupus e outras condições autoimunes."
# )
# print(inserir_especialidade(especialidade))

# print(obter_todas_especialidades())
# print(obter_especialidade_por_id(1))
# print(atualizar_especialidade(especialidade = Especialidade(
#     idEspecialidade=1,  # ID da especialidade a ser atualizada
#     nome="Endocrinologia",
#     descricao="Especialidade médica que se concentra no diagnóstico e tratamento de distúrbios hormonais e metabólicos, como diabetes, problemas da tireoide e obesidade."
# )))

# print(deletar_especialidade(1))

# print(inserir_medicamento(Medicamento(
#     idMedicamento=0,  # será gerado automaticamente
#     nome="BUscopan",
# )))

# print(obter_todos_medicamentos())
# print(obter_medicamento_por_id(1))
# print(atualizar_medicamento(Medicamento(
#     idMedicamento=1,  # ID do medicamento a ser atualizado
#     nome="Neosaldina"
# )))
# print(deletar_medicamento(1))

# print(inserir_consulta(Consulta(
#     idConsulta=0,  # será gerado automaticamente
#     idMedico=20,  # ID do médico
#     idPaciente=9,  # ID do paciente
#     dataHora="2023-10-01 10:00:00",
#     queixa="Dor de cabeça frequente",
#     conduta="Prescrever analgésicos e solicitar exames"
# )))

# print(obter_todas_consultas())
# print(obter_consulta_por_id(1))

# print(atualizar_consulta(Consulta(
#     idConsulta=1,  # ID da consulta a ser atualizada
#     idMedico=20,  # ID do médico
#     idPaciente=5,  # ID do paciente
#     dataHora="2023-10-01 10:00:00",
#     queixa="Perna quebrada",
#     conduta="Prescrever analgésicos e solicitar exames"
# )))

# print(deletar_consulta(3))

# print(inserir_entrada_prontuario(EntradaProntuario(
#     idProntuario=0,  # será gerado automaticamente
#     idConsulta=2,  # ID da consulta associada
#     data="2023-10-01",
#     queixaPrincipal="Dor no joelho",
#     alergias="Nenhuma",
#     solicitacoesExames="Raio-X do joelho",
#     antecedentesFamiliares="Nenhum",
#     fatoresAlivio="Repouso e compressa fria",
#     fatoresPiora="Movimentação excessiva",
#     fatoresPredecessores="Atividade física intensa"
# )))

# print(obter_todas_entradas_prontuario())
# print(obter_entrada_prontuario_por_id(1))
# print(atualizar_entrada_prontuario(EntradaProntuario(
#     idProntuario=1,  # ID da entrada de prontuário a ser atualizada
#     idConsulta=1,  # ID da consulta associada
#     data="2023-10-01",
#     queixaPrincipal="Dor na barriga",
#     alergias="todas",
#     solicitacoesExames="Raio-X do joelho",
#     antecedentesFamiliares="Nenhum",
#     fatoresAlivio="Repouso e compressa fria",
#     fatoresPiora="Movimentação excessiva",
#     fatoresPredecessores="Atividade física intensa"
# )))

# print(deletar_entrada_prontuario(2))

# print(inserir_medico_especialidade(MedicoEspecialidade(
#     idMedico=20,  # ID do médico)
#     idEspecialidade=2,  # ID da especialidade
#     dataHabilitacao="2023-10-01"
# )))


# print(inserir_medico_especialidade(MedicoEspecialidade(
#     idMedico=25,  # ID do médico
#     idEspecialidade=3,  # ID da especialidade
#     dataHabilitacao="2023-10-01"
# )))
      

# print(atualizar_medico_especialidade(MedicoEspecialidade(
#     idMedico=24,  # ID do médico)
#     idEspecialidade=2,  # ID da especialidade
#     dataHabilitacao="2023-10-80"
# )))

# print(obter_todos_medicos_especialidades())
# print(obter_medico_especialidade_por_id(20, 2))
# print(deletar_medico_especialidade(25, 3))

# print(inserir_item_receita(ItemReceita(
#     idConsulta=2,  # ID da consulta associada
#     idMedicamento=3,  # ID do medicamento
#     descricao="Tomar 1 comprimido a cada 8 horas"
# )))

# print(obter_todos_itens_receita())  
# print(obter_item_receita_por_id(1, 2))
# print(atualizar_item_receita(ItemReceita(
#     idConsulta=1,  # ID da consulta associada  
#     idMedicamento=2,  # ID do medicamento
#     descricao="Tomar 1 comprimido a cada 6 horas"
# )))

# print(deletar_item_receita(2, 3))



# print(inserir_agenda(Agenda(
#     idAgenda=0,  # será gerado automaticamente
#     idMedico=24,  # ID de um médico existente
#     dataHora="2025-06-21 10:00:00",
#     disponivel=True
# )))

# Consultar todas as agendas
# print(obter_todas_agendas())

# Consultar agenda por ID
# print(obter_agenda_por_id(1))

# Atualizar agenda
# print(atualizar_agenda(Agenda(
#     idAgenda=1,  # ID da agenda a ser atualizada
#     idMedico=20,
#     dataHora="2025-06-21 17:00:00",
#     disponivel=False
# )))

# Deletar agenda
# print(deletar_agenda(3))



# print(inserir_agendamento(Agendamento(
#     idAgendamento=0,  # será gerado automaticamente
#     idPaciente=5,  # ID de um paciente existente
#     status="Pendente",
#     dataAgendamento="2025-06-21 10:00:00"
# )))

# print(obter_todos_agendamentos())
# print(obter_agendamento_por_id(1))

# print(atualizar_agendamento(Agendamento(
#     idAgendamento=1,  # ID do agendamento a ser atualizado
#     idPaciente=15,  # ID do paciente associado
#     status="Confirmado",
#     dataAgendamento="2025-06-21 10:00:00"
# )))

# print(deletar_agendamento(2))
