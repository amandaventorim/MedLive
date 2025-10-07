#!/usr/bin/env python3
"""
Gerador de CPFs válidos para teste
"""

def calcular_digito_cpf(cpf_parcial):
    """Calcula um dígito verificador do CPF"""
    soma = sum(int(cpf_parcial[i]) * (len(cpf_parcial) + 1 - i) for i in range(len(cpf_parcial)))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

def gerar_cpf_valido(base):
    """Gera um CPF válido a partir de uma base de 9 dígitos"""
    # Garantir que a base tenha 9 dígitos
    base = str(base).zfill(9)
    
    # Calcular primeiro dígito verificador
    primeiro_digito = calcular_digito_cpf(base)
    
    # Calcular segundo dígito verificador
    segundo_digito = calcular_digito_cpf(base + str(primeiro_digito))
    
    # CPF completo
    cpf_completo = base + str(primeiro_digito) + str(segundo_digito)
    
    # Formatar com máscara
    cpf_formatado = f"{cpf_completo[:3]}.{cpf_completo[3:6]}.{cpf_completo[6:9]}-{cpf_completo[9:]}"
    
    return cpf_completo, cpf_formatado

if __name__ == "__main__":
    print("CPFs válidos para teste:")
    print("=" * 40)
    
    bases_teste = [
        123456789,
        987654321,
        456789123,
        789123456,
        321654987
    ]
    
    for base in bases_teste:
        cpf_numerico, cpf_formatado = gerar_cpf_valido(base)
        print(f"Base: {base:09d} -> CPF: {cpf_numerico} ou {cpf_formatado}")