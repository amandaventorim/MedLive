import sqlite3

def verificar_disponibilidade():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Verificar estrutura da tabela correta
    print('=== ESTRUTURA DA TABELA DISPONIBILIDADE_MEDICO ===')
    cursor.execute("PRAGMA table_info(disponibilidade_medico)")
    colunas = cursor.fetchall()
    for col in colunas:
        print(f'Coluna: {col[1]}, Tipo: {col[2]}')

    # Verificar dados existentes
    print('\n=== DADOS DA TABELA DISPONIBILIDADE_MEDICO ===')
    cursor.execute('SELECT * FROM disponibilidade_medico')
    disponibilidades = cursor.fetchall()
    if disponibilidades:
        for disp in disponibilidades:
            print(disp)
    else:
        print('❌ Nenhuma disponibilidade encontrada!')
        
        # Inserir disponibilidades para Urias (ID 3)
        print('\n💡 Inserindo disponibilidades para Urias...')
        disponibilidades_urias = [
            (3, 'Segunda', '08:00', '12:00'),
            (3, 'Segunda', '14:00', '18:00'),
            (3, 'Terça', '08:00', '12:00'),
            (3, 'Terça', '14:00', '18:00'),
            (3, 'Quarta', '08:00', '12:00'),
            (3, 'Quarta', '14:00', '18:00'),
            (3, 'Quinta', '08:00', '12:00'),
            (3, 'Quinta', '14:00', '18:00'),
            (3, 'Sexta', '08:00', '12:00'),
            (3, 'Sexta', '14:00', '18:00'),
        ]

        for disp in disponibilidades_urias:
            try:
                cursor.execute('''
                    INSERT INTO disponibilidade_medico (idMedico, diaSemana, horaInicio, horaFim)
                    VALUES (?, ?, ?, ?)
                ''', disp)
            except Exception as e:
                print(f'Erro ao inserir {disp}: {e}')
        
        conn.commit()
        print(f'✅ Disponibilidades inseridas!')

        # Verificar novamente
        cursor.execute('SELECT * FROM disponibilidade_medico WHERE idMedico = 3')
        disp_urias = cursor.fetchall()
        print(f'\n=== DISPONIBILIDADES DO URIAS ===')
        for disp in disp_urias:
            print(f'ID: {disp[0]}, Médico: {disp[1]}, Dia: {disp[2]}, Horário: {disp[3]}-{disp[4]}')

    conn.close()

if __name__ == "__main__":
    verificar_disponibilidade()