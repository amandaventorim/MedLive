#!/usr/bin/env python3
"""
Teste de validação de endereços
"""
from dto import CriarPacienteDTO

def testar_enderecos():
    enderecos_teste = [
        'Rua A',                    # Muito curto
        'Rua B, 123',               # Curto
        'Rua Teste, 123 - SP',      # Médio mas ainda curto
        'Rua Teste, 123 - Centro - São Paulo - SP',  # Longo o suficiente
    ]

    for i, endereco in enumerate(enderecos_teste):
        try:
            dto = CriarPacienteDTO(
                nome='Teste Usuario Silva',
                cpf='11144477735',
                email=f'teste{i}@email.com',
                senha='senha123',
                genero='feminino',
                dataNascimento='1990-05-15',
                endereco=endereco,
                convenio='Unimed'
            )
            print(f'Endereço "{endereco}" ({len(endereco)} chars) -> VÁLIDO')
        except Exception as e:
            print(f'Endereço "{endereco}" ({len(endereco)} chars) -> ERRO: {e}')

if __name__ == "__main__":
    testar_enderecos()