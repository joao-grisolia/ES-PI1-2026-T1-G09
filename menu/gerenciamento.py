import os
import time
import sistema.candidato as candidato
import sistema.eleitor as eleitor
import menu.menu_principal as menu
from funcoes import ascii


def gerenciamento(conn):
    '''
    controla o menu de gerenciamento do sistema

    permite acessar as funcionalidades de gestao de eleitores,
    gestao de candidatos ou voltar ao menu principal

    Args:
        conn (mysql.connector): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: nao retorna nenhum valor
    '''
    os.system('cls')
    time.sleep(0.5)
    ascii.gerenciamentoASCII()
    n = 0
    #Adiciondo while que impede a digitação de opção inválida.
    while n !=1 and n !=2 and n !=3:
        print('''
          1. Gestão de Eleitores
          2. Gestão de Candidatos
          3. Voltar
          ''')
        n = int(input('-> '))
        if n !=1 and n !=2 and n !=3:
            print("Digite um valor válido!")

    if n == 1:
        eleitor.gestao_eleitores(conn)
    elif n == 2:
        candidato.gestao_candidatos(conn)
    elif n == 3:
        menu.menu(conn)