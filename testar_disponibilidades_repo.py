import sys
sys.path.append('.')

from data.repo.disponibilidade_medico_repo import obter_disponibilidades_por_medico

def testar_disponibilidades():
    print("🔍 Testando obter_disponibilidades_por_medico")
    
    try:
        disponibilidades = obter_disponibilidades_por_medico(3)  # Urias
        print(f"✅ Disponibilidades encontradas: {len(disponibilidades)}")
        
        for disp in disponibilidades:
            print(f"  - Dia: {disp.diaSemana}, Horário: {disp.horaInicio}-{disp.horaFim}, Ativo: {disp.ativo}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_disponibilidades()