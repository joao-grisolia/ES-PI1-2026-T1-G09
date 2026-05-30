import os
import menu.gerenciamento as gerenciamento
from funcoes import ascii
import menu.votacao as votacao
import time

def menu(conn):
    '''
    controla o menu principal do sistema

    exibe o menu inicial que vai para o modulo de 
    gerenciamento, votacao ou encerramento

    Args:
        conn (mysql.connector): Conexão ativa com o banco de dados MySQL.

    Returns:
        None: nao retorna nenhum valor
    '''
    os.system('cls')
    time.sleep(0.5)
    ascii.menuASCII()
    #Adicionado while que evita a digitação de opção inválida!
    n = 0
    while n !=1 and n !=2 and n !=3:
        print('''
        1. Gerenciamento
        2. Votação
        3. Sair
        ''')
        n = int(input("-> "))
        if n !=1 and n !=2 and n!=3:
            print("Digite uma opção válida!")
    if n == 1:
        gerenciamento.gerenciamento(conn)
    elif n == 2:
        votacao.votacao(conn)
    elif n == 3:
        print("Sistema encerrado")
        