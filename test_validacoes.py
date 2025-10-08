#!/usr/bin/env python3
"""
Teste das validações do DTO para verificar se as mensagens de erro estão funcionando
"""

from dto.usuario_dtos import CriarUsuarioDTO
from pydantic import ValidationError

def test_validacoes():
    print("=== TESTANDO VALIDAÇÕES DO DTO ===\n")
    
    # Teste 1: Nome vazio
    print("1. Testando nome vazio...")
    try:
        usuario = CriarUsuarioDTO(
            nome='',
            cpf='123.456.789-09',
            email='teste@test.com',
            senha='123456',
            genero='masculino',
            dataNascimento='1990-01-01'
        )
        print("❌ ERRO: Deveria ter falhado!")
    except ValidationError as e:
        print("✅ Validação funcionou:")
        for error in e.errors():
            print(f"   Campo: {error['loc'][0]}, Erro: {error['msg']}")
    print()

    # Teste 2: CPF inválido
    print("2. Testando CPF inválido...")
    try:
        usuario = CriarUsuarioDTO(
            nome='João Silva',
            cpf='111.111.111-11',
            email='teste@test.com',
            senha='123456',
            genero='masculino',
            dataNascimento='1990-01-01'
        )
        print("❌ ERRO: Deveria ter falhado!")
    except ValidationError as e:
        print("✅ Validação funcionou:")
        for error in e.errors():
            print(f"   Campo: {error['loc'][0]}, Erro: {error['msg']}")
    print()

    # Teste 3: Email inválido
    print("3. Testando email inválido...")
    try:
        usuario = CriarUsuarioDTO(
            nome='João Silva',
            cpf='123.456.789-09',
            email='email_invalido',
            senha='123456',
            genero='masculino',
            dataNascimento='1990-01-01'
        )
        print("❌ ERRO: Deveria ter falhado!")
    except ValidationError as e:
        print("✅ Validação funcionou:")
        for error in e.errors():
            print(f"   Campo: {error['loc'][0]}, Erro: {error['msg']}")
    print()

    # Teste 4: Senha muito curta
    print("4. Testando senha muito curta...")
    try:
        usuario = CriarUsuarioDTO(
            nome='João Silva',
            cpf='123.456.789-09',
            email='teste@test.com',
            senha='123',
            genero='masculino',
            dataNascimento='1990-01-01'
        )
        print("❌ ERRO: Deveria ter falhado!")
    except ValidationError as e:
        print("✅ Validação funcionou:")
        for error in e.errors():
            print(f"   Campo: {error['loc'][0]}, Erro: {error['msg']}")
    print()

    # Teste 5: Data inválida
    print("5. Testando data inválida...")
    try:
        usuario = CriarUsuarioDTO(
            nome='João Silva',
            cpf='123.456.789-09',
            email='teste@test.com',
            senha='123456',
            genero='masculino',
            dataNascimento='data_invalida'
        )
        print("❌ ERRO: Deveria ter falhado!")
    except ValidationError as e:
        print("✅ Validação funcionou:")
        for error in e.errors():
            print(f"   Campo: {error['loc'][0]}, Erro: {error['msg']}")
    print()

    print("=== TESTE DE VALIDAÇÃO CONCLUÍDO ===")

if __name__ == "__main__":
    test_validacoes()