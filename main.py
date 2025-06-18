from data.model.usuario_model import Usuario
from data.repo.usuario_repo import *
from data.model.paciente_model import Paciente
from data.repo.paciente_repo import *


# Criar tabelas
criar_tabela_usuario()
criar_tabela_paciente()

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

# Atualizar o paciente
# print("\n🔄 Atualizando endereço e convênio do paciente...")
# atualizar_paciente( paciente = Paciente(
#     idPaciente=9,
#     idUsuario=9,  
#     nome=usuario.nome,
#     cpf=usuario.cpf,
#     email=usuario.email,
#     senha=usuario.senha,
#     genero=usuario.genero,
#     dataNascimento=usuario.dataNascimento,
#     endereco="Avenida Brasil, 456",
#     convenio="Bradesco Saúde"
# ))

# # Verificar atualização
# print("\n✅ Pacientes após atualização:")
# for p in obter_todos_pacientes():
#     print(p)

paciente = Paciente(
    idPaciente=0,  # será definido automaticamente
    idUsuario=0,   # também
    nome="Ana Clara",
    cpf="11122233344",
    email="ana@email.com",
    senha="123456",
    genero="Feminino",
    dataNascimento="2000-01-01",
    endereco="Rua A, 123",
    convenio="Unimed"
)
registrar_paciente_completo(paciente)