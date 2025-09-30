import sqlite3

def listar_tabelas():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Listar todas as tabelas
    print('=== TODAS AS TABELAS DO BANCO ===')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    for tabela in tabelas:
        print(f'Tabela: {tabela[0]}')

    # Procurar tabelas com "disponibilidade" no nome
    print('\n=== TABELAS COM "DISPONIBILIDADE" ===')
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%disponibilidade%'")
    tabelas_disp = cursor.fetchall()
    for tabela in tabelas_disp:
        print(f'Tabela: {tabela[0]}')

    if not tabelas_disp:
        print('❌ Nenhuma tabela de disponibilidade encontrada!')
        print('\n💡 Vamos criar a tabela de disponibilidade...')
        
        # Criar tabela de disponibilidade
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disponibilidadeMedico (
                idDisponibilidade INTEGER PRIMARY KEY AUTOINCREMENT,
                idMedico INTEGER NOT NULL,
                diaSemana TEXT NOT NULL,
                horaInicio TEXT NOT NULL,
                horaFim TEXT NOT NULL,
                FOREIGN KEY (idMedico) REFERENCES medico(idMedico)
            )
        ''')
        conn.commit()
        print('✅ Tabela disponibilidadeMedico criada!')

        # Inserir algumas disponibilidades de teste para Urias (ID 3)
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

        cursor.executemany('''
            INSERT INTO disponibilidadeMedico (idMedico, diaSemana, horaInicio, horaFim)
            VALUES (?, ?, ?, ?)
        ''', disponibilidades_urias)
        conn.commit()
        print(f'✅ Inseridas {len(disponibilidades_urias)} disponibilidades para Urias!')

        # Verificar se inseriu corretamente
        cursor.execute('SELECT * FROM disponibilidadeMedico WHERE idMedico = 3')
        disp_urias = cursor.fetchall()
        print(f'\n=== DISPONIBILIDADES DO URIAS ===')
        for disp in disp_urias:
            print(f'ID: {disp[0]}, Médico: {disp[1]}, Dia: {disp[2]}, Horário: {disp[3]}-{disp[4]}')

    conn.close()

if __name__ == "__main__":
    listar_tabelas()