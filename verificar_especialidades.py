#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar especialidades no banco de dados
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.repo.especialidade_repo import obter_todas_especialidades

def verificar_especialidades():
    print("🔍 Verificando especialidades no banco de dados...")
    print("=" * 50)
    
    try:
        especialidades = obter_todas_especialidades()
        
        print(f"📊 Total de especialidades: {len(especialidades)}")
        print()
        
        if especialidades:
            for i, esp in enumerate(especialidades, 1):
                print(f"{i}. ID: {esp.idEspecialidade}")
                print(f"   Nome: {esp.nome}")
                print(f"   Descrição: {esp.descricao}")
                print()
        else:
            print("❌ Nenhuma especialidade encontrada no banco de dados")
            print("💡 Use o painel de administração para cadastrar especialidades")
        
    except Exception as e:
        print(f"❌ Erro ao acessar banco: {e}")

if __name__ == "__main__":
    verificar_especialidades()