from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *
from data.model.medico_model import Medico
from data.repo.medico_repo import *
from data.model.administrador_model import Administrador
from data.repo.administrador_repo import *



# Criar tabelas
criar_tabela_usuario()
criar_tabela_paciente()
criar_tabela_medico()
criar_tabela_administrador()    

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

medico = Medico(
    idMedico=0,  # será gerado automaticamente
    idUsuario=0,  # igual ao idMedico
    nome="Guilherme",
    cpf="44466677788",
    email="carlos.medico@email.com",
    senha="med123",
    genero="Masculino",
    dataNascimento="1980-06-25",
    crm="CRM123456",
    statusProfissional="Ativo"
)

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
administrador = Administrador(
    idAdministrador=0,  # será gerado automaticamente
    idUsuario=0,
    nome="Catarina",
    cpf="99988877766",
    email="fernanda.admin@email.com",
    senha="admin123",
    genero="Feminino",
    dataNascimento="1985-10-12"
)

# # Inserir administrador (usuário + administrador)
# id_admin = inserir_usuario_administrador(administrador)
# print(f"✅ Administrador inserido com sucesso! ID: {id_admin}")

# # Consultar todos os administradores
# print("\n👩‍💼 Administradores no sistema:")
# for a in obter_todos_administradores():
#     print(a)

# Consultar administrador por ID
# print(obter_administrador_por_id(23))


# Deletar administrador + usuário
print("\n🗑️ Deletando administrador:")
print(deletar_usuario_administrador(23))