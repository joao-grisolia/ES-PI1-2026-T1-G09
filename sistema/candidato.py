import os
import time
import menu.menu_principal as menu
import menu.gerenciamento as gerenciamento

def gestao_candidatos(conn):
            """
            Esta função exibe um menu de opções para gerenciar os candidatos em um sistema eleitoral. 
            O usuário pode escolher entre cadastrar, editar, buscar ou listar candidatos, ou voltar ao menu principal. 
            A função utiliza uma conexão ativa com um banco de dados MySQL para realizar as operações necessárias.

            Args:
                conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

            Returns:
                None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console. 

            """
            os.system('cls')
            time.sleep(0.5)
            print('''
            \nDigite o número da opção desejada.

            1. Cadastrar Candidato
            2. Editar Candidato
            3. Buscar Candidato
            4. Listar Candidatos
            5. Voltar
            ''')
            try:
                n = int(input("-> "))
                if (n == 1):
                    cadastrar_candidato(conn)
                elif (n == 2):
                    os.system('cls')
                    editar_candidato(conn)
                elif (n == 3):
                    os.system('cls')
                    buscar_candidato(conn)
                elif (n == 4):
                    # melhorar a exibicao dos candidatos
                    # deixar mais bonito 
                    os.system('cls')
                    listar_candidatos(conn)
                    input('\nPressione ENTER para voltar.')
                    gestao_candidatos(conn)
                elif (n == 5):
                    os.system('cls')
                    gerenciamento.gerenciamento(conn)
                else:
                    print("Opção inválida. Tente novamente.")
                    input("\nPressione ENTER para continuar.")
                    gestao_candidatos(conn)
            except ValueError:
                print("Opção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar.")
                gestao_candidatos(conn)

def verificarNumCadidato(conn, numCandidato):
    cursor = conn.cursor()
    try:
        cursor.execute('''
                    SELECT COUNT(*)
                    FROM candidatos
                    WHERE numero_votacao = %s
                    ''', (numCandidato,))
        if cursor.fetchone()[0] > 0:
            print('Já existe um candidato com esse número')
            input("Pressione ENTER para voltar.")
            return True
        else:
            return False
    finally:
        cursor.close()


# implementar a verificação para não adicionar
# um candidato com o mesmo número e partido...
def cadastrar_candidato(conn):
    """
    Esta função permite ao usuário cadastrar um novo candidato em um sistema eleitoral. 
    O usuário é solicitado a fornecer o nome, número de votação, partido e opcionalmente uma foto ASCII do candidato.
    A função realiza validações para garantir que a foto ASCII seja adequada e, em seguida,
    insere os dados do candidato no banco de dados MySQL.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console. 

    """ 
    try:
        cursor = conn.cursor()
        os.system('cls')
        time.sleep(0.5)
        name = str(input('Digite o nome do candidato: '))
        number = int(input('Digite o número do candidato: '))
        if verificarNumCadidato(conn, number):
            print('Voltando, aguarde...')
            time.sleep(1.7)
            return
        partido = str(input('Digite o partido do candidato: '))
        
        fotoASCII = str(input('Deseja adicionar foto ASCII para o candidato (s/n): ')).lower()
        while fotoASCII != 's' and fotoASCII != 'n':
            print('Digite somente "s" ou "n"')
            fotoASCII = str(input('Deseja adicionar foto ASCII para o candidato (s/n): ')).lower()
            
        asciiFOTO = None
        pastaASCII = None
        
        if fotoASCII == 's':
            
            repetir = 's'
            while repetir == 's':   
                os.system('cls')
                print("\nCole a arte ASCII (digite FIM para terminar):\n")
                
                linhas = []
                linha = ''
                while linha != 'FIM' :
                    linha = input()
                    if linha != 'FIM':
                        linhas.append(linha)
                
                '''
                    nesses if sao validacoes simples para ver se o cara nao ta adicionando qualquer coisa
                    1. verifico o numero de linhas se for muito pequeno eu ja invalido
                    2. verifico o numero de colunas para ver se o desenho nao vai ficar muito estreito, se for
                    muito pequeno ja invalido tbm
                    3. depois eu verifico se o cara ta digitando pelo menos 100 caracteres
                    4. peço pra confirmar e salvo na pasta ascii com o numero dele, ai no banco, eu salvo o
                    caminho da pasta, para ficar associado a foto com o candidato
                '''
                
                if len(linhas) < 5:  
                    print('\nASCII muito pequeno!')
                    input('Pressione ENTER para tentar novamente')
                    continue
                
                maior_linha = 0
                for linha in linhas:
                    tamanho = len(linha)
                    
                    if tamanho > maior_linha:
                        maior_linha = tamanho
                
                if maior_linha < 20:
                    print('\nASCII muito pequeno!')
                    input('Pressione ENTER para tentar novamente')
                    continue
                
                
                contador = 0
                for linha in linhas:
                    for caracter in linha:
                        if caracter != ' ':
                            contador +=1 
                
                if contador < 100:
                    print('\nASCII inválido')
                    input('Pressione ENTER para tentar novamente')
                    continue
                
                os.system('cls')
                print('\nPré Vizualizacao')
                print('\n'.join(linhas))
                
                confirmar = str(input('\nConfirmar ASCII (s/n): ')).lower()
                while confirmar != 's' and confirmar != 'n':
                    print('Digite somente "s" ou "n"')
                    confirmar = input('Deseja adicionar foto ASCII (s/n): ').lower()
                if confirmar != 's':
                    print('\nRefaça o ASCII')
                    input('Pressione ENTER')
                    continue
                    
                asciiFOTO = '\n'.join(linhas)
                pastaASCII = f'ascii/ascii_candidato{number}.txt'

                with open(pastaASCII, 'w', encoding='utf-8') as f:
                    f.write(asciiFOTO)
                    
                repetir = 'n'
        
        sql = 'INSERT INTO candidatos (nome_completo, numero_votacao, nome_partido, foto_ascii) VALUES (%s, %s, %s, %s)'
        val = (name, number, partido, pastaASCII)

        cursor.execute(sql, val)
        conn.commit()
        
        print("\nCandidato cadastrado!\n")
        input('Pressione ENTER para voltar.')
    finally:
        cursor.close()

    gestao_candidatos(conn)



def editar_candidato(conn):
    """
    Esta função permite ao usuário editar as informações de um candidato existente em um sistema eleitoral.
    O usuário é solicitado a fornecer o nome do candidato que deseja editar. Se o candidato for encontrado, suas informações atuais são exibidas,
    e o usuário pode inserir um novo nome, número de votação e partido para o candidato.
    A função então atualiza as informações do candidato no banco de dados MySQL.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console.  

    """
    try:
        time.sleep(0.5)
        cursor = conn.cursor()
        nome = str(input("Digite o nome do candidato que deseja alterar: "))
        sql = 'SELECT * FROM candidatos'
        cursor.execute(sql)
        result = cursor.fetchall()

        '''
                na nossa tabela candidatos tem os campos
                id    nome   numero   partido
                0      1       2        3
                entao os indice no for fica assim
                id e o indice 0, nome e o indice 1, numero e o indice 2 e partido e o indice 3
                por isso do candidato[1]
                pq ele percorre todos os candidatos
                se algum cadidato tiver o nome igual ele vai pro if

                resumindo, o for faz o seguinte
                
                para cada candidato na tabela candidatos (ele pega todos os candidatos)
                se o nome digitado for igual ao nome do candidato (candidato[1])
                fecho acho o homi  
        '''
        encontrado = False
        for candidato in result:
            if nome == candidato[1]:
                encontrado = True
                print(f"\nCandidato encontrado: {candidato[1]} | Número: {candidato[2]} | Partido: {candidato[3]}\n")
                name = str(input("Digite um novo nome para o candidato: "))
                number = int(input("Digite o número do partido: "))
                partido = str(input("Digite o nome do partido: "))

                sql = 'UPDATE candidatos SET nome_completo=%s, numero_votacao=%s, nome_partido=%s WHERE id=%s'
                values = (name, number, partido, candidato[0])

                cursor.execute(sql, values)
                conn.commit()

                print("\nCandidato alterado!")
                input("\nPressione ENTER para voltar.")
                gestao_candidatos(conn)
                break
        
        if not encontrado:
            print("\nCandidato não encontrado.\n")
            input("Pressione ENTER para voltar.")
            gestao_candidatos(conn)
    finally:
        cursor.close()

def buscar_candidato(conn):
    """
        Esta função permite ao usuário buscar um candidato específico em um sistema eleitoral, utilizando o número candidato como critério de busca.
        O usuário é solicitado a inserir o número do partido do candidato que deseja encontrar.
        A função então consulta o banco de dados MySQL para obter uma lista de todos os candidatos 
        e verifica se algum deles possui o número de partido correspondente.
        Se um candidato for encontrado, suas informações são exibidas no console, incluindo o nome, número e partido,
        bem como uma foto ASCII associada, se disponível. Caso nenhum candidato seja encontrado com o número de partido fornecido,
        uma mensagem informando que nenhum candidato foi encontrado é exibida.

        Args:
            conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

        Returns:
            None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console.  

    """
    try:
        time.sleep(0.5)
        cursor = conn.cursor()
        numeroPartido = int(input("\nDigite o numero do candidato: "))
        sql = 'SELECT * FROM candidatos'
        cursor.execute(sql)
        result = cursor.fetchall()
        
        encontrado = False
        print("\nCandidatos encontrados:\n")
        print('-' * 120)
        
        for candidato in result:
            if numeroPartido == candidato[2]:
                encontrado = True
                
                if len(candidato) > 4 and candidato[4]:
                    try:
                        with open(candidato[4], 'r', encoding='utf-8') as f:
                            print(f.read())
                    except:
                        print('Erro ao carregar ASCII')
                else:
                    print('Sem Imagem')
                    
                print(f"Nome: {candidato[1]} | Número: {candidato[2]} | Partido: {candidato[3]}")
                
        if not encontrado:
            print('Nenhum candidato encontrado')
        print('-' * 120)
        input('\nPressione ENTER para voltar.')
    finally:
        cursor.close()
    gestao_candidatos(conn)

def listar_candidatos(conn):
    """
    Esta função consulta o banco de dados para obter uma lista de todos os candidatos registrados em um sistema eleitoral,
    exibindo suas informações no console.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console.
    """
    try:
        time.sleep(0.5)
        cursor = conn.cursor()
        sql = 'SELECT * FROM candidatos'
        cursor.execute(sql)
        result = cursor.fetchall()

        print('Cadastrando candidato, aguarde...')
        time.sleep(1.7)
        print("\nCandidatos cadastrados:\n")
        print('-' * 120)
        for candidato in result:
            print(f"Nome: {candidato[1]} | Número: {candidato[2]} | Partido: {candidato[3]}")
        print('-' * 120)
    finally:
        cursor.close()


    


