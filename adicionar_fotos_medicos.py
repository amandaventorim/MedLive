import sqlite3

def adicionar_fotos_medicos():
    """
    Script para adicionar fotos de exemplo aos médicos cadastrados
    """
    conn = sqlite3.connect('dados.db')
    cursor = conn.cursor()

    # Verificar médicos existentes
    print('=== MÉDICOS CADASTRADOS ===')
    cursor.execute("""
        SELECT m.idMedico, u.nome, u.foto 
        FROM medico m 
        JOIN usuario u ON m.idMedico = u.idUsuario
    """)
    medicos = cursor.fetchall()
    
    if not medicos:
        print('❌ Nenhum médico encontrado no sistema!')
        return
    
    for medico in medicos:
        id_medico, nome, foto_atual = medico
        status_foto = "✅ Com foto" if foto_atual else "❌ Sem foto"
        print(f'ID: {id_medico}, Nome: {nome}, Foto: {status_foto}')
    
    print('\n=== ADICIONANDO FOTOS DE EXEMPLO ===')
    
    # Fotos placeholder usando o serviço UI Avatars (gera avatars automáticos)
    fotos_exemplo = {
        # Usando serviço que gera avatars baseados no nome
        # Formato: https://ui-avatars.com/api/?name=Nome+Sobrenome&size=200&background=001942&color=fff
    }
    
    # Para cada médico sem foto, adicionar uma foto placeholder
    for medico in medicos:
        id_medico, nome, foto_atual = medico
        
        if not foto_atual:  # Se não tem foto
            # Gerar URL do avatar baseado no nome
            nome_url = nome.replace(' ', '+')
            foto_url = f"https://ui-avatars.com/api/?name={nome_url}&size=200&background=001942&color=fff&bold=true"
            
            # Atualizar no banco
            cursor.execute("UPDATE usuario SET foto = ? WHERE idUsuario = ?", (foto_url, id_medico))
            print(f'✅ Foto adicionada para {nome}: {foto_url}')
        else:
            print(f'⚠️  {nome} já possui foto: {foto_atual}')
    
    conn.commit()
    
    # Verificar resultado final
    print('\n=== RESULTADO FINAL ===')
    cursor.execute("""
        SELECT m.idMedico, u.nome, u.foto 
        FROM medico m 
        JOIN usuario u ON m.idMedico = u.idUsuario
    """)
    medicos_atualizados = cursor.fetchall()
    
    for medico in medicos_atualizados:
        id_medico, nome, foto = medico
        print(f'✅ {nome}: {foto}')
    
    conn.close()
    print('\n🎉 Fotos adicionadas com sucesso!')
    print('\n💡 As fotos são avatars automáticos gerados pelo UI Avatars.')
    print('   Para usar fotos reais, substitua as URLs pelos caminhos das fotos locais.')

if __name__ == "__main__":
    adicionar_fotos_medicos()