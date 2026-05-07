def zerezima(conn):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tabela_votos') # apaga tudao da tabela voto
    cursor.execute('ALTER TABLE tabela_votos AUTO_INCREMENT = 1') 
    cursor.execute('UPDATE eleitores SET status_voto = 0 WHERE status_voto = 1')
    conn.commit()
    
    cursor.execute('''
        SELECT c.nome_completo, c.numero_votacao, c.nome_partido, COUNT(v.id_candidato) as total
        FROM candidatos c
        LEFT JOIN tabela_votos v ON c.id = v.id_candidato
        GROUP BY c.id
        ORDER BY total DESC
    ''') # busca os cara
    
    candidatos = cursor.fetchall()
    for i in candidatos:
        print(f'{i[1]} - {i[0]} ({i[2]}) --> {i[3]} votos')
        
    print('\t\tZerézima Aplicada\n')