import os
import time
import menu.gerenciamento as gerenciamento
import funcoes.criptografia as criptografia
import mysql.connector
from funcoes import ascii as ascii
from funcoes.criptografia import criptografia
from funcoes.descriptografia import descriptografia
from funcoes.chaveDeAcesso import gerar_chave_acesso
from funcoes.validacaoCPF import (
    validar_cpf,
    limpar_cpf,
    verificarCpfDuplicado
)
from funcoes.validacao_TituloEleitor import (
    validar_titulo_eleitor,
    verificarTituloDeEleitorDuplicado
)

def gestao_eleitores(conn):
    """
            Esta função exibe um menu para a gestão de eleitores, permitindo ao usuário escolher entre cadastrar um novo eleitor,
            editar ou remover um eleitor existente, buscar eleitores por nome, listar todos os eleitores ou voltar para o menu de gerenciamento.
            A função interage com o banco de dados MySQL para realizar as operações necessárias, como verificar duplicidade de CPF e título de eleitor,
            e inserir novos registros na tabela de eleitores.

            Args:
                conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

            Returns:
                None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console. 

    """
    os.system('cls')
    time.sleep(0.5)
    
    print('''
        Digite o número da opção desejada:

        1. Cadastrar Eleitor
        2. Editar Eleitor
        3. Buscar Eleitor
        4. Listar Eleitores
        5. Voltar
    ''')
    try:
        n = int(input("-> "))
        
        if (n == 1):
            cadastrar_eleitor(conn)
        elif (n == 2):
            editarEleitor(conn)
        elif (n == 3):
            buscar_eleitores(conn)
            input("\nPressione ENTER para voltar.")
            gestao_eleitores(conn)
        elif (n == 4):
            listar_eleitores(conn)
            input("\nPressione ENTER para voltar.")
            gestao_eleitores(conn)

        elif (n == 5):
            os.system('cls')
            gerenciamento.gerenciamento(conn)
        else:
            print("Opção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar.")
            gestao_eleitores(conn)
            
    except ValueError:
        print("Opção inválida. Tente novamente.")
        input("\nPressione ENTER para continuar.")
        gestao_eleitores(conn)

def cadastrar_eleitor(conn):
    """
    Esta função permite cadastrar um novo eleitor no sistema, solicitando ao usuário informações como nome completo,
    CPF, título de eleitor e se atuará como mesário. A função valida o CPF e o título de eleitor,
    verifica se já existem registros com o mesmo CPF ou título no banco de dados, e, se tudo estiver correto,
    insere um novo registro na tabela de eleitores com as informações fornecidas.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console. 

    """
    os.system('cls')
    time.sleep(0.5)
    nome_completo = str(input("Digite seu nome completo: "))

    cpf = str(input("Digite seu CPF: "))

    while not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        cpf = str(input("Digite seu CPF: "))

    cpf = limpar_cpf(cpf)
    if verificarCpfDuplicado(conn, cpf):
        print('Voltando, aguarde...')
        time.sleep(1.7)
        gestao_eleitores(conn)
        

    titulo_eleitor = str(input("Digite seu título de eleitor: "))
    while validar_titulo_eleitor(titulo_eleitor) == False:
        print("Título de eleitor inválido. Tente novamente:")
        titulo_eleitor = str(input("Digite seu título de eleitor: "))
    
    if verificarTituloDeEleitorDuplicado(conn, titulo_eleitor):
        print('Voltando, aguarde...')
        time.sleep(1.7)
        gestao_eleitores(conn)

    n = 0
    while n!=1 and n!=2:
        print('''
        Você atuará como mesário?
        1. Sim
        2. Não
            ''')
        n = int(input("-> "))
        if n!=1 and n!=2:
            print("Digite uma opção válida!")

    if n == 1:
        mesario = 1
    elif n == 2:
        mesario = 0
    else:
        print("Opção inválida. Tente novamente.")
        return

    status_voto = 0
    chave_normal = gerar_chave_acesso(nome_completo)
    print('Cadastrando eleitor, aguarde...')
    time.sleep(1.7)
    print(f"Chave de acesso gerada: {chave_normal}")

    cpf_criptografado = criptografia(cpf)
    chave_acesso = criptografia(chave_normal)


    try: 
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO eleitores (chave_acesso, nome_completo, titulo_eleitor, cpf_criptografado, mesario, status_voto)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (chave_acesso, nome_completo, titulo_eleitor, cpf_criptografado, mesario, status_voto))
        conn.commit()
        
        print("Eleitor cadastrado com sucesso")
    except mysql.connector.IntegrityError as e:
        print(f"\nErro ao cadastrar: {e}")
    finally:
        cursor.close()
        input("\nPressione ENTER para voltar.")
        gestao_eleitores(conn)

def editarEleitor(conn):
    """
    Esta função permite editar as informações de um eleitor existente no sistema. O usuário é solicitado a fornecer o nome completo do eleitor que deseja editar,
    e a função consulta o banco de dados MySQL para encontrar um eleitor com o nome correspondente. 
    Se o eleitor for encontrado, o usuário pode inserir um novo nome para o eleitor, e a função atualiza o registro no banco de dados com o novo nome fornecido.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console.

    """
    os.system('cls')
    time.sleep(0.5)
    cursor = conn.cursor()
    cpf = str(input("\nDigite o CPF do eleitor: ")).strip()
    

    while not validar_cpf(cpf):
        print("CPF inválido. Tente novamente.")
        cpf = str(input("Digite o CPF do eleitor: "))
    cpf = limpar_cpf(cpf)
    cpf_criptografado = criptografia(cpf)
    
    cursor.execute('''SELECT * 
            FROM eleitores
            WHERE cpf_criptografado = %s
            ''', (cpf_criptografado,))
    result = cursor.fetchall()
    
    print('Buscando eleitor, aguarde...')
    time.sleep(1.7)

    encontrado = False

    for eleitor in result:
        if cpf_criptografado == eleitor[4]:
            encontrado = True
            
            print("\nEleitor encontrado!")
            cpf_descriptografado = (descriptografia(str(eleitor[4])))
            chave_descriptografada = (descriptografia(str(eleitor[1])))
            cpf_descriptografado = cpf_descriptografado[:11]
            chave_descriptografada = chave_descriptografada[:7]
            print(f"Nome: {eleitor[2]} |", f"Chave de acesso: {chave_descriptografada} |", f"Título de eleitor: {eleitor[3]} |", f"CPF: {cpf_descriptografado} |", f"Mesário: {eleitor[5]}")

            print('''
                    Qual informação deseja alterar:\n
                        1. NOME
                        2. CPF
                        3. TITULO DE ELEITOR
                        4. STATUS MESARIO
                        5. VOLTAR
                ''')
            opcao = int(input('-> '))
            
            match opcao:
                case 1:
                    nome = str(input("\nDigite o novo NOME para o eleitor: "))
                    sql = 'UPDATE eleitores SET nome_completo = %s WHERE id = %s'
                    values = (nome, eleitor[0])
                    cursor.execute(sql, values)
                
                case 2:
                    cpf = str(input("\nDigite o novo CPF para o eleitor: "))
                    
                    while not validar_cpf(cpf):
                        print("CPF inválido. Tente novamente.")
                        cpf = str(input("Digite o novo CPF para o eleitor: "))
                    cpf = limpar_cpf(cpf)

                    if verificarCpfDuplicado(conn, cpf):
                        print('Voltando, aguarde...')
                        time.sleep(1.7)
                        gestao_eleitores(conn)
                    else:
                        values = (criptografia(cpf), eleitor[0])
                        sql = 'UPDATE eleitores SET cpf_criptografado = %s WHERE id = %s'
                        cursor.execute(sql, values)
                        cursor.close()

                case 3:
                    tituloDeEleitor = str(input("\nDigite o novo TITULO DE ELEITOR para o eleitor: "))
                    while validar_titulo_eleitor(tituloDeEleitor) == False:
                        print("Título de eleitor inválido. Tente novamente:")
                        tituloDeEleitor = str(input("Digite o novo TITULO DE ELEITOR para o eleitor: "))

                    if verificarTituloDeEleitorDuplicado(conn, tituloDeEleitor):
                        print('Voltando, aguarde...')
                        time.sleep(1.7)
                        gestao_eleitores(conn)
                    else:
                        values = (tituloDeEleitor, eleitor[0])
                        sql = 'UPDATE eleitores SET titulo_eleitor = %s WHERE id = %s'
                        cursor.execute(sql, values)
                        cursor.close()
                        
                
                case 4:
                    if eleitor[5] == 0:
                        print(f'\nDeseja COLOCAR {eleitor[2]} como MESÁRIO? (s/n)')
                    else:
                        print(f'\nDeseja REMOVER {eleitor[2]} como MESÁRIO? (s/n)')

                    opcao = str(input('-> ')).strip().lower()
                    while opcao not in ('s', 'sim', 'n', 'não', 'nao'):
                        print('Digite somente SIM ou NAO')
                        opcao = str(input('-> ')).strip().lower()

                    if opcao in ('s', 'sim'):
                        novo_status = 1 if eleitor[5] == 0 else 0
                        cursor.execute('UPDATE eleitores SET mesario = %s WHERE id = %s', (novo_status, eleitor[0]))
                    else:
                        print('Alteração de status de mesario CANCELADA')
                        print('Voltando, aguarde...')
                        time.sleep(2.2)
                        gestao_eleitores(conn)
                    
                    
            conn.commit()

            print('Alterando eleitor, aguarde...')
            time.sleep(1.7)
            input("\nEleitor alterado com sucesso. Pressione ENTER para voltar.\n")
            gestao_eleitores(conn)
            break

    if not encontrado:
        n = input("\nEleitor não encontrado. Pressione ENTER para voltar.\n")
        gestao_eleitores(conn)

def buscar_eleitores(conn):
    """
        Esta função permite buscar eleitores no sistema com base no CPF ou Titulo de eleitor. 
        Ela consulta o banco de dados MySQL para encontrar eleitores cujo CPF ou Titulo de eleitor contenham no banco de dados,
        e exibe os resultados formatados no console.

        Args:
            conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

        Returns:
            None: A função não retorna nenhum valor, apenas exibe os resultados no console. 

    """
    os.system('cls')
    time.sleep(0.5)
    
    cursor = conn.cursor()
    
    print('''\nDeseja buscar o eleitor por CPF ou Titulo:\n
            1. CPF
            2. Título de Eleitor
            3. Voltar
          ''')
    
    n = int(input("-> "))
    
    while n!=1 and n!=2 and n!=3:
        print('''\nOpção inválida. Digite:\n
            1. CPF
            2. Título de Eleitor
            3. Voltar
        ''')
        n = int(input('-> '))
    
    if n == 1:
        cpf = str(input("\nDigite o CPF do eleitor: ")).strip()

        while not validar_cpf(cpf):
            print("CPF inválido. Tente novamente.")
            cpf = str(input("Digite o CPF do eleitor: "))
        cpf_criptografado = criptografia(cpf)
        
        cursor.execute('''SELECT * 
                FROM eleitores
                WHERE cpf_criptografado = %s
                ''', (cpf_criptografado,))
        result = cursor.fetchall()
    
    elif n == 2:
        titulo = str(input('\nDigite o Titulo de eleitor: '))
        
        while not validar_titulo_eleitor(titulo):
            print('Titulo de eleitor invalido. Tente novamente')
            titulo = int(input('Digite o Titulo de eleitor: '))
        
        cursor.execute('''SELECT * 
                FROM eleitores
                WHERE titulo_eleitor = %s
                ''', (titulo,))
        result = cursor.fetchall()
    
    elif n ==3:
        gestao_eleitores(conn)
    
    # ---           --- #
    
    print('Buscando eleitores, aguarde...')
    time.sleep(1.7)
    
    print("\nEleitores encontrados:\n")
    print('-' * 150)
    
    for eleitor in result:
        cpf_descriptografado = (descriptografia(str(eleitor[4])))
        chave_descriptografada = (descriptografia(str(eleitor[1])))
        cpf_descriptografado = cpf_descriptografado[:11]
        chave_descriptografada = chave_descriptografada[:7]
        print(f"Nome: {eleitor[2]} |", f"Chave de acesso: {chave_descriptografada} |", f"Título de eleitor: {eleitor[3]} |", f"CPF: {cpf_descriptografado} |", f"Mesário: {eleitor[5]} |", f"Status do voto: {eleitor[6]}")
    print('-' * 150)

def listar_eleitores(conn):
    """
    Esta função consulta o banco de dados para obter uma lista de todos os eleitores registrados em um sistema eleitoral, exibindo suas informações no console.

    Args:
        conn (mysql.connector.connection_cext.CMySQLConnection): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: A função não retorna nenhum valor, apenas exibe os resultados e interage com o usuário por meio do console.

    """
    os.system('cls')
    time.sleep(0.5)
    cursor = conn.cursor()
    sql = "SELECT * FROM eleitores"
    cursor.execute(sql)
    result = cursor.fetchall()

    print('Listando eleitores, aguarde...')
    time.sleep(1.7)
    print("Lista de eleitores:")
    print('-' * 150)
    for eleitor in result:
        cpf_descriptografado = (descriptografia(str(eleitor[4])))
        chave_descriptografada = (descriptografia(str(eleitor[1])))
        cpf_descriptografado = cpf_descriptografado[:11]
        chave_descriptografada = chave_descriptografada[:7]
        print(f"Nome Completo: {eleitor[2]} | Chave de Acesso: {chave_descriptografada} | Título de Eleitor: {eleitor[3]} | CPF: {cpf_descriptografado} | Mesário: {eleitor[5]} | Status do Voto: {eleitor[6]}")
    print('-' * 150)


