import sqlite3

def verificar_dados():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Verificar médicos cadastrados
    print('=== MÉDICOS CADASTRADOS ===')
    cursor.execute('SELECT idMedico, nome FROM medico')
    medicos = cursor.fetchall()
    for medico in medicos:
        print(f'ID: {medico[0]}, Nome: {medico[1]}')

    print('\n=== DISPONIBILIDADES CADASTRADAS ===')
    cursor.execute('SELECT * FROM disponibilidadeMedico')
    disponibilidades = cursor.fetchall()
    if disponibilidades:
        for disp in disponibilidades:
            print(f'ID: {disp[0]}, Médico: {disp[1]}, Dia: {disp[2]}, Horário: {disp[3]}-{disp[4]}')
    else:
        print('Nenhuma disponibilidade encontrada!')
    
    # Verificar especificamente o médico Urias
    print('\n=== DADOS ESPECÍFICOS DO URIAS ===')
    cursor.execute("SELECT idMedico, nome FROM medico WHERE nome LIKE '%Urias%'")
    urias = cursor.fetchone()
    if urias:
        print(f'Urias encontrado - ID: {urias[0]}, Nome: {urias[1]}')
        
        cursor.execute("SELECT * FROM disponibilidadeMedico WHERE idMedico = ?", (urias[0],))
        disp_urias = cursor.fetchall()
        if disp_urias:
            print('Disponibilidades do Urias:')
            for disp in disp_urias:
                print(f'  Dia: {disp[2]}, Horário: {disp[3]}-{disp[4]}')
        else:
            print('❌ Urias não tem disponibilidades cadastradas!')
    else:
        print('❌ Médico Urias não encontrado!')

    conn.close()

if __name__ == "__main__":
    verificar_dados()