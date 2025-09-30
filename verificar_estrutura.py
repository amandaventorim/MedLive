import sqlite3

def verificar_estrutura():
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Verificar estrutura da tabela medico
    print('=== ESTRUTURA DA TABELA MEDICO ===')
    cursor.execute("PRAGMA table_info(medico)")
    colunas_medico = cursor.fetchall()
    for col in colunas_medico:
        print(f'Coluna: {col[1]}, Tipo: {col[2]}')

    # Verificar estrutura da tabela usuario (médicos podem estar aí)
    print('\n=== ESTRUTURA DA TABELA USUARIO ===')
    cursor.execute("PRAGMA table_info(usuario)")
    colunas_usuario = cursor.fetchall()
    for col in colunas_usuario:
        print(f'Coluna: {col[1]}, Tipo: {col[2]}')

    # Verificar dados das tabelas
    print('\n=== DADOS DA TABELA MEDICO ===')
    cursor.execute('SELECT * FROM medico LIMIT 5')
    medicos = cursor.fetchall()
    for medico in medicos:
        print(medico)

    print('\n=== USUÁRIOS MÉDICOS ===')
    cursor.execute("SELECT * FROM usuario WHERE perfil = 'medico' LIMIT 5")
    usuarios_medicos = cursor.fetchall()
    for usuario in usuarios_medicos:
        print(usuario)

    # Verificar disponibilidades
    print('\n=== ESTRUTURA DA TABELA DISPONIBILIDADEMEDICO ===')
    cursor.execute("PRAGMA table_info(disponibilidadeMedico)")
    colunas_disp = cursor.fetchall()
    for col in colunas_disp:
        print(f'Coluna: {col[1]}, Tipo: {col[2]}')

    print('\n=== DADOS DA TABELA DISPONIBILIDADEMEDICO ===')
    cursor.execute('SELECT * FROM disponibilidadeMedico LIMIT 10')
    disponibilidades = cursor.fetchall()
    for disp in disponibilidades:
        print(disp)

    conn.close()

if __name__ == "__main__":
    verificar_estrutura()