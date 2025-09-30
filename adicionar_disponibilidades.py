import sqlite3

def adicionar_disponibilidades_urias():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Adicionar disponibilidades para Urias (ID 3) em mais dias
    print('=== ADICIONANDO MAIS DISPONIBILIDADES PARA URIAS ===')
    
    novas_disponibilidades = [
        (3, 2, '08:00', '12:00'),  # Terça manhã
        (3, 2, '14:00', '18:00'),  # Terça tarde
        (3, 3, '08:00', '12:00'),  # Quarta manhã
        (3, 3, '14:00', '18:00'),  # Quarta tarde
        (3, 4, '08:00', '12:00'),  # Quinta manhã
        (3, 4, '14:00', '18:00'),  # Quinta tarde
    ]
    
    dias_semana = {
        1: 'Segunda-feira',
        2: 'Terça-feira', 
        3: 'Quarta-feira',
        4: 'Quinta-feira',
        5: 'Sexta-feira',
        6: 'Sábado',
        7: 'Domingo'
    }
    
    for disp in novas_disponibilidades:
        try:
            cursor.execute('''
                INSERT INTO disponibilidade_medico (idMedico, diaSemana, horaInicio, horaFim, ativo)
                VALUES (?, ?, ?, ?, 1)
            ''', disp)
            dia_nome = dias_semana.get(disp[1])
            print(f'✅ Adicionado: {dia_nome} {disp[2]}-{disp[3]}')
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                dia_nome = dias_semana.get(disp[1])
                print(f'⚠️  Já existe: {dia_nome} {disp[2]}-{disp[3]}')
            else:
                print(f'❌ Erro: {e}')
    
    conn.commit()
    
    # Verificar todas as disponibilidades do Urias
    print('\n=== TODAS AS DISPONIBILIDADES DO URIAS ===')
    cursor.execute('SELECT * FROM disponibilidade_medico WHERE idMedico = 3 ORDER BY diaSemana, horaInicio')
    disponibilidades = cursor.fetchall()
    
    for disp in disponibilidades:
        dia_nome = dias_semana.get(disp[2])
        ativo = "✅" if disp[5] else "❌"
        print(f'{ativo} {dia_nome}: {disp[3]}-{disp[4]}')
    
    conn.close()

if __name__ == "__main__":
    adicionar_disponibilidades_urias()