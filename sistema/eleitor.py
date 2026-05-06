import os
import menu.gerenciamento as gerenciamento
import funcoes.chaveDeAcesso as chaveDeAcesso
from funcoes.chaveDeAcesso import gerar_chave_acesso
import funcoes.criptografia as criptografia
import funcoes.validacaoCPF as validacaoCPF
from funcoes import ascii as ascii
from funcoes.validacaoCPF import primeiros_quatro_digitos
from database.conexao import conectar
import mysql.connector
from funcoes.criptografia import criptografia
from funcoes.validacaoCPF import validar_cpf
from funcoes.validacao_TituloEleitor import validar_titulo_eleitor

'''
    por enquanto nenhuma funcao esta implementada
    aqui tem que fazer tudo, e tem a parte  da criptograffia
    e a parte de validao do cpf criacao da chave de acesso
    tem umas coisinha aqui
    
    eu fiz 3 arquivos na pasta funcoes
    chaveDeAcesso.py
    criptografia.py
    validacaoCPF.py
    
    ai usa esses arquivos para fazer a logica
    e fazer funfar    
    essas funcoes fazem na hora de cadastrar um eleitor
    criptografar a chave de acesso, validar o cpf e criar a chave de acesso
    
    na parte de editar, tem que solicitar o cpf do eleitor
    a senha dele,  tudo dele, pq se nao ele pode editar o usuario de outra pessoa
    
    ai buscar e listar, acredito que seja ja opcao de adm, pq nao faz sentido
    um eleitor buscar outro ou listar tlgd? entao faz essa validao antes
    igual no candidato que tem essa validacao de adm    
'''

conexao = conectar()
cursor = conexao.cursor()

def gestao_eleitores():
            os.system('cls')
            
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

                    os.system('cls')

                    def cadastrar_eleitor():
                        nome_completo = str(input("Digite seu nome completo: "))
                        
                        cpf = str(input("Digite seu CPF: "))
                        while validar_cpf(cpf) ==False:
                            print("CPF inválido. Tente novamente: ")
                            cpf = str(input("Digite seu CPF: "))
                        print("CPF válido!")
                        
                        
                        conn = conectar()
                        cursor = conn.cursor()
                        verificarCpfDuplicado = criptografia(cpf)
                        
                        try:
                            '''
                                pra verificar se ja tem cpf, eu to criptografando dnv o cpf que o cara digitou
                                ai executa o sql pra ver o seguinte:
                                "SELECT COUNT(*) FROM eleitores WHERE cpf_criptografado = %s", (verificarCpfDuplicado,)
                                ou seja
                                quantas linhas tem na tabela eleitores com o cpf criptografado igual ao cpf que o cara digitou 

                                se for 1 ou por algum motivo desconhecido maior que 1, entao ja tem um cpf igual no banco
                            '''
                            cursor.execute("SELECT COUNT(*) FROM eleitores WHERE cpf_criptografado = %s", (verificarCpfDuplicado,))
                            if cursor.fetchone()[0] > 0:
                                '''
                                entra no if, com isso oq o fetchone faz?
                                resumindo pega o resultado que o banco retornou
                                no caso o COUNT(*) contou da tabela eleitors quantos cpf iguais aquele que o cara digitou ele achou
                                
                                se o indice [0]  (oq o fetchone retorna) for maior que 0, entao ja existe no banco o cpf que a pessoa digitou
                                retorna erro e volta pro gestao_eleitores
                                '''
                                print("\nCPF ja cadastrado")
                                cursor.close()
                                conn.close()
                                input("Pressione ENTER para voltar.")
                                gestao_eleitores()
                                return
                        finally:
                            cursor.close()
                            conn.close()
                        
                        titulo_eleitor = str(input("Digite seu título de eleitor: "))
                        while validar_titulo_eleitor(titulo_eleitor) == False:
                            print("Título de eleitor inválido. Tente novamente:")
                            titulo_eleitor = str(input("Digite seu título de eleitor: "))
                        print("Título válido!")
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
                        print(f"Chave de acesso gerada: {chave_normal}")
                        
                        cpf_criptografado = criptografia(cpf)
                        chave_acesso = criptografia(chave_normal)
                        conn = conectar()
                        
                        try: 
                            cursor = conn.cursor()
                            
                            cursor.execute('''
                                INSERT INTO eleitores (chave_acesso, nome_completo, titulo_eleitor, cpf_criptografado, mesario, status_voto)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            ''', (chave_acesso, nome_completo, titulo_eleitor, cpf_criptografado, mesario, status_voto))
                            conn.commit()
                            print("eleitor cadastrado com sucesso")
                        except mysql.connector.IntegrityError as e:
                            print(f"\nErro ao cadastrar: {e}")
                        finally:
                            cursor.close()
                            conn.close()
                            input("\nPressione ENTER para voltar.")
                            gestao_eleitores()
                    cadastrar_eleitor()

                elif (n == 2):
                    os.system('cls')
                    def editar_remover_eleitor():
                        
                        nome = str(input("Digite o nome completo do eleitor que deseja editar: "))
                        sql = 'SELECT * FROM eleitores'
                        cursor.execute(sql)
                        result = cursor.fetchall()

                        encontrado = False

                        for eleitor in result:
                            if nome == eleitor[2]:
                                encontrado = True

                                print("\nEleitor encontrado!")

                                nome = str(input("Digite o novo nome para o candidato: "))
                                sql = 'UPDATE eleitores SET nome_completo = %s WHERE id = %s'
                                values = (nome, eleitor[0])

                                cursor.execute(sql, values)
                                conexao.commit()

                                n = input("\nEleitor alterado com sucesso. Pressione ENTER para voltar.\n")
                                gestao_eleitores()
                                break

                        if not encontrado:
                            n = input("\nEleitor não encontrado. Pressione ENTER para voltar.\n")
                            gestao_eleitores()

                    editar_remover_eleitor()

                elif (n == 3):
                    os.system('cls')
                    def buscar_eleitores():

                        conexao = conectar()
                        cursor = conexao.cursor()
                        
                        nome = str(input("\nDigite o nome do eleitor: ")).strip()
                        sql = "SELECT * FROM eleitores WHERE LOWER(nome_completo) LIKE ?"
                        cursor.execute(sql, (f"%{nome.lower()}%",))
                        result = cursor.fetchall()
                        
                        print("\nEleitores encontrados:\n")
                        print('-' * 120)
                        for eleitor in result:
                            print(f"Nome: {eleitor[2]}")
                        print('-' * 120)
                        input('\nPressione ENTER para voltar.')
                    buscar_eleitores()
                    input("\nPressione ENTER para voltar.")
                    gestao_eleitores()

                elif (n == 4):

                    os.system('cls')

                    def listar_eleitores():
                        conexao = conectar()
                        cursor = conexao.cursor()
                        
                        input("\nPressione ENTER para listar todos os eleitores.")
                        sql = "SELECT * FROM eleitores"
                        cursor.execute(sql)
                        result = cursor.fetchall()

                        print("Lista de eleitores:")
                        print('-' * 150)
                        for eleitor in result:
                            print(f"Nome Completo: {eleitor[2]} | Chave de Acesso: {eleitor[1]} | Título de Eleitor: {eleitor[3]} | CPF Criptografado: {eleitor[4]} | Mesário: {eleitor[5]} | Status do Voto: {eleitor[6]}")
                        print('-' * 150)

                    listar_eleitores()
                    input("\nPressione ENTER para voltar.")
                    gestao_eleitores()

                elif (n == 5):
                    os.system('cls')
                    gerenciamento.gerenciamento()
                else:
                    print("Opção inválida. Tente novamente.")
                    input("\nPressione ENTER para continuar.")
                    gestao_eleitores()
                    
            except ValueError:
                print("Opção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar.")
                gestao_eleitores()
