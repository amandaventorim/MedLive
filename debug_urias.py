import sqlite3
from datetime import datetime

def debug_urias():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Dados do Urias
    print('=== DADOS DO URIAS ===')
    cursor.execute("SELECT idUsuario, nome FROM usuario WHERE nome LIKE '%urias%'")
    urias_usuario = cursor.fetchone()
    print(f'Usuário: ID {urias_usuario[0]}, Nome: {urias_usuario[1]}')

    cursor.execute("SELECT idMedico FROM medico WHERE idMedico = ?", (urias_usuario[0],))
    urias_medico = cursor.fetchone()
    if urias_medico:
        print(f'Médico: ID {urias_medico[0]}')
    else:
        print('❌ Urias não encontrado na tabela médico!')
        return

    # Disponibilidades do Urias
    print('\n=== DISPONIBILIDADES DO URIAS ===')
    cursor.execute('SELECT * FROM disponibilidade_medico WHERE idMedico = ?', (urias_medico[0],))
    disponibilidades = cursor.fetchall()
    
    dias_semana = {
        1: 'Segunda-feira',
        2: 'Terça-feira', 
        3: 'Quarta-feira',
        4: 'Quinta-feira',
        5: 'Sexta-feira',
        6: 'Sábado',
        7: 'Domingo'
    }
    
    for disp in disponibilidades:
        dia_nome = dias_semana.get(disp[2], f'Dia {disp[2]}')
        print(f'ID: {disp[0]}, Dia: {disp[2]} ({dia_nome}), Horário: {disp[3]}-{disp[4]}, Ativo: {disp[5]}')

    # Testar conversão de dia da semana para uma data específica
    print('\n=== TESTE DE CONVERSÃO DE DIAS ===')
    data_teste = datetime(2025, 10, 1)  # 1 de outubro de 2025
    dia_python = data_teste.weekday()  # 0=Monday, 6=Sunday
    dia_banco = dia_python + 1
    
    print(f'Data teste: {data_teste.strftime("%Y-%m-%d %A")}')
    print(f'Dia Python: {dia_python}')
    print(f'Dia Banco: {dia_banco}')
    print(f'Nome do dia: {dias_semana.get(dia_banco, "Desconhecido")}')
    
    # Verificar se Urias trabalha neste dia
    cursor.execute('SELECT * FROM disponibilidade_medico WHERE idMedico = ? AND diaSemana = ? AND ativo = 1', 
                   (urias_medico[0], dia_banco))
    disp_dia = cursor.fetchall()
    
    if disp_dia:
        print(f'✅ Urias trabalha na {dias_semana.get(dia_banco)}:')
        for disp in disp_dia:
            print(f'  Horário: {disp[3]}-{disp[4]}')
    else:
        print(f'❌ Urias NÃO trabalha na {dias_semana.get(dia_banco)}')

    conn.close()

if __name__ == "__main__":
    debug_urias()