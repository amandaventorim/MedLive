#!/usr/bin/env python3
"""
Script para criar a tabela de disponibilidade do médico
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.repo.disponibilidade_medico_repo import criar_tabela_disponibilidade_medico

def main():
    print("Criando tabela de disponibilidade do médico...")
    
    try:
        resultado = criar_tabela_disponibilidade_medico()
        
        if resultado:
            print("✅ Tabela 'disponibilidade_medico' criada com sucesso!")
        else:
            print("❌ Erro ao criar tabela 'disponibilidade_medico'")
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
