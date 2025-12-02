#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug das especialidades - comparar banco x página
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.repo.especialidade_repo import obter_todas_especialidades

def debug_especialidades():
    print("🔍 DEBUG: Especialidades - Banco vs Página")
    print("=" * 60)
    
    try:
        # Buscar especialidades da mesma forma que a rota
        especialidades = obter_todas_especialidades()
        
        print(f"📊 Total encontrado pela função: {len(especialidades)}")
        print()
        
        print("📋 Lista completa:")
        for i, esp in enumerate(especialidades, 1):
            print(f"{i:2d}. [ID:{esp.idEspecialidade:2d}] {esp.nome}")
            print(f"     Descrição: {esp.descricao}")
            
            # Verificar se tem algum caractere especial que pode estar causando problema
            nome_clean = esp.nome.strip().lower()
            print(f"     Nome normalizado: '{nome_clean}'")
            
            if nome_clean in ['clinica geral', 'clínica geral', 'psiquiatria']:
                print(f"     ⚠️  ESTA é uma das especialidades que não aparece!")
            print()
        
        # Verificar se há algum problema específico
        nomes_problema = []
        for esp in especialidades:
            nome = esp.nome.strip().lower()
            if nome in ['clinica geral', 'clínica geral', 'psiquiatria']:
                nomes_problema.append(esp.nome)
        
        print("🚨 DIAGNÓSTICO:")
        if nomes_problema:
            print(f"   Especialidades 'problemáticas' ENCONTRADAS no banco:")
            for nome in nomes_problema:
                print(f"   - {nome}")
            print("   ✅ O problema NÃO está na busca do banco")
            print("   ⚠️  O problema pode estar na renderização HTML ou JavaScript")
        else:
            print("   ❌ Especialidades 'problemáticas' NÃO encontradas no banco")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_especialidades()