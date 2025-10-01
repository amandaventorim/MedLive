"""
Exemplos de uso dos DTOs do MedLive
Este arquivo demonstra como usar os DTOs implementados
"""

from dto import (
    CriarUsuarioDTO, CriarMedicoDTO, CriarPacienteDTO,
    LoginUsuarioDTO, AgendarConsultaDTO
)
from pydantic import ValidationError
import json


def exemplo_usuario_valido():
    """Exemplo de criação de usuário com dados válidos"""
    print("=== Exemplo: Usuário Válido ===")
    
    try:
        usuario_dto = CriarUsuarioDTO(
            nome="João Silva Santos",
            cpf="123.456.789-01",
            email="joao@email.com",
            senha="senha123",
            genero="masculino",
            dataNascimento="1990-05-15",
            perfil="paciente"
        )
        
        print("✅ DTO criado com sucesso!")
        print(f"Nome: {usuario_dto.nome}")
        print(f"CPF: {usuario_dto.cpf}")
        print(f"Email: {usuario_dto.email}")
        print(f"JSON: {usuario_dto.to_json()}")
        
    except ValidationError as e:
        print("❌ Erro de validação:")
        for erro in e.errors():
            print(f"  - {erro['msg']}")


def exemplo_usuario_invalido():
    """Exemplo de criação de usuário com dados inválidos"""
    print("\n=== Exemplo: Usuário Inválido ===")
    
    try:
        usuario_dto = CriarUsuarioDTO(
            nome="J",  # Muito curto
            cpf="123.456.789-00",  # CPF inválido
            email="email-invalido",  # Email inválido
            senha="123",  # Senha muito curta
            genero="indefinido",  # Gênero não existe
            dataNascimento="2020-01-01",  # Menor de idade
            perfil="paciente"
        )
        
    except ValidationError as e:
        print("❌ Erros encontrados (como esperado):")
        for erro in e.errors():
            campo = erro.get('loc', [''])[0]
            mensagem = erro['msg']
            if mensagem.startswith("Value error, "):
                mensagem = mensagem.replace("Value error, ", "")
            print(f"  - {campo}: {mensagem}")


def exemplo_medico_valido():
    """Exemplo de criação de médico com dados válidos"""
    print("\n=== Exemplo: Médico Válido ===")
    
    try:
        medico_dto = CriarMedicoDTO(
            nome="Dr. Carlos Ferreira Silva",
            cpf="987.654.321-00",
            email="dr.carlos@clinica.com",
            senha="senha123",
            genero="masculino",
            dataNascimento="1980-03-20",
            crm="CRM/SP-123456",
            statusProfissional="ativo"
        )
        
        print("✅ DTO de médico criado com sucesso!")
        print(f"Nome: {medico_dto.nome}")
        print(f"CRM: {medico_dto.crm}")
        print(f"Status: {medico_dto.statusProfissional}")
        print(f"Perfil: {medico_dto.perfil}")  # Deve ser "medico"
        
    except ValidationError as e:
        print("❌ Erro de validação:")
        for erro in e.errors():
            print(f"  - {erro['msg']}")


def exemplo_paciente_valido():
    """Exemplo de criação de paciente com dados válidos"""
    print("\n=== Exemplo: Paciente Válido ===")
    
    try:
        paciente_dto = CriarPacienteDTO(
            nome="Maria Santos Silva",
            cpf="111.222.333-44",
            email="maria@email.com",
            senha="senha123",
            genero="feminino",
            dataNascimento="1985-07-12",
            endereco="Rua das Flores, 123 - Centro - São Paulo - SP",
            convenio="Unimed Nacional"
        )
        
        print("✅ DTO de paciente criado com sucesso!")
        print(f"Nome: {paciente_dto.nome}")
        print(f"Endereço: {paciente_dto.endereco}")
        print(f"Convênio: {paciente_dto.convenio}")
        print(f"Perfil: {paciente_dto.perfil}")  # Deve ser "paciente"
        
    except ValidationError as e:
        print("❌ Erro de validação:")
        for erro in e.errors():
            print(f"  - {erro['msg']}")


def exemplo_login():
    """Exemplo de login"""
    print("\n=== Exemplo: Login ===")
    
    try:
        login_dto = LoginUsuarioDTO(
            email="usuario@email.com",
            senha="senha123"
        )
        
        print("✅ DTO de login criado com sucesso!")
        print(f"Email: {login_dto.email}")
        
    except ValidationError as e:
        print("❌ Erro de validação:")
        for erro in e.errors():
            print(f"  - {erro['msg']}")


def exemplo_agendamento():
    """Exemplo de agendamento de consulta"""
    print("\n=== Exemplo: Agendamento ===")
    
    try:
        agendamento_dto = AgendarConsultaDTO(
            medico_id=1,
            data_consulta="2025-10-15",
            horario_consulta="14:30",
            observacoes="Consulta de rotina"
        )
        
        print("✅ DTO de agendamento criado com sucesso!")
        print(f"Médico ID: {agendamento_dto.medico_id}")
        print(f"Data: {agendamento_dto.data_consulta}")
        print(f"Horário: {agendamento_dto.horario_consulta}")
        print(f"Observações: {agendamento_dto.observacoes}")
        
    except ValidationError as e:
        print("❌ Erro de validação:")
        for erro in e.errors():
            print(f"  - {erro['msg']}")


def exemplo_agendamento_invalido():
    """Exemplo de agendamento com dados inválidos"""
    print("\n=== Exemplo: Agendamento Inválido ===")
    
    try:
        agendamento_dto = AgendarConsultaDTO(
            medico_id=0,  # ID inválido
            data_consulta="2024-01-01",  # Data no passado
            horario_consulta="20:00",  # Horário fora do comercial
            observacoes="x" * 600  # Observações muito longas
        )
        
    except ValidationError as e:
        print("❌ Erros encontrados (como esperado):")
        for erro in e.errors():
            campo = erro.get('loc', [''])[0]
            mensagem = erro['msg']
            if mensagem.startswith("Value error, "):
                mensagem = mensagem.replace("Value error, ", "")
            print(f"  - {campo}: {mensagem}")


def main():
    """Executa todos os exemplos"""
    print("🧪 TESTANDO DTOs DO MEDLIVE")
    print("=" * 50)
    
    exemplo_usuario_valido()
    exemplo_usuario_invalido()
    exemplo_medico_valido()
    exemplo_paciente_valido()
    exemplo_login()
    exemplo_agendamento()
    exemplo_agendamento_invalido()
    
    print("\n" + "=" * 50)
    print("✅ Todos os testes concluídos!")


if __name__ == "__main__":
    main()