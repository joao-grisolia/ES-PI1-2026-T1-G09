import os
import menu.gerenciamento as gerenciamento
from funcoes.chaveDeAcesso import gerar_chave_acesso
import funcoes.criptografia as criptografia
from funcoes.descriptografia import descriptografia
from funcoes import ascii as ascii
from funcoes.validacaoCPF import primeiros_quatro_digitos
from database.conexao import conectar
import mysql.connector
from funcoes.criptografia import criptografia
from funcoes.validacaoCPF import validar_cpf, limpar_cpf
from funcoes.validacao_TituloEleitor import validar_titulo_eleitor
from funcoes import registrar_log

conexao = conectar()
cursor = conexao.cursor()

def gestao_eleitores(conn):
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

                    def cadastrar_eleitor(conn):
                        nome_completo = str(input("Digite seu nome completo: "))
                        
                        cpf = str(input("Digite seu CPF: "))

                        while not validar_cpf(cpf):
                            print("CPF inválido. Tente novamente.")
                            cpf = str(input("Digite seu CPF: "))
                        
                        cpf = limpar_cpf(cpf)
                        print("CPF válido!")
                        
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
                                input("Pressione ENTER para voltar.")
                                gestao_eleitores(conn)
                                return
                        finally:
                            cursor.close()

                        titulo_eleitor = str(input("Digite seu título de eleitor: "))
                        while validar_titulo_eleitor(titulo_eleitor) == False:
                            print("Título de eleitor inválido. Tente novamente:")
                            titulo_eleitor = str(input("Digite seu título de eleitor: "))
                        print("Título válido!")

                        cursor = conn.cursor()
                        try:
                            '''
                                pra verificar se ja tem titulo,
                                executa o sql pra ver o seguinte:
                                "SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s", (titulo_eleitor,)
                                ou seja
                                quantas linhas tem na tabela eleitores com o titulo eleitor igual ao titulo que o cara digitou 

                                se for 1 ou por algum motivo desconhecido maior que 1, entao ja tem um titulo igual no banco
                            '''
                            cursor.execute("SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s", (titulo_eleitor,))
                            if cursor.fetchone()[0] > 0:
                                '''
                                entra no if, com isso oq o fetchone faz?
                                resumindo pega o resultado que o banco retornou
                                no caso o COUNT(*) contou da tabela eleitors quantos titulo iguais aquele que o cara digitou ele achou
                                
                                se o indice [0]  (oq o fetchone retorna) for maior que 0, entao ja existe no banco o titulo que a pessoa digitou
                                retorna erro e volta pro gestao_eleitores
                                '''
                                print("\nTítulo de eleitor ja cadastrado")
                                input("Pressione ENTER para voltar.")
                                gestao_eleitores(conn)
                                return
                        finally:
                            cursor.close()

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
                            input("\nPressione ENTER para voltar.")
                            gestao_eleitores(conn)
                    cadastrar_eleitor(conn)

                elif (n == 2):
                    os.system('cls')
                    def editar_remover_eleitor(conn):
                        
                        cursor = conn.cursor()
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
                                conn.commit()

                                n = input("\nEleitor alterado com sucesso. Pressione ENTER para voltar.\n")
                                gestao_eleitores(conn)
                                break

                        if not encontrado:
                            n = input("\nEleitor não encontrado. Pressione ENTER para voltar.\n")
                            gestao_eleitores(conn)

                    editar_remover_eleitor(conn)

                elif (n == 3):
                    os.system('cls')
                    def buscar_eleitores(conn):

                        cursor = conn.cursor()
                        
                        nome = str(input("\nDigite o nome do eleitor: ")).strip()
                        sql = "SELECT * FROM eleitores WHERE LOWER(nome_completo) LIKE %s"
                        cursor.execute(sql, ('%' + nome.lower() + '%',))
                        result = cursor.fetchall()
                        
                        print("\nEleitores encontrados:\n")
                        print('-' * 150)
                        for eleitor in result:
                            print(f"Nome: {eleitor[2]} |", f"Chave de acesso: {eleitor[1]} |", f"Título de eleitor: {eleitor[3]} |", f"CPF Criptografado: {eleitor[4]} |", f"Mesário: {eleitor[5]} |", f"Status do voto: {eleitor[6]}")
                        print('-' * 150)
                        
                    buscar_eleitores(conn)
                    input("\nPressione ENTER para voltar.")
                    gestao_eleitores(conn)

                elif (n == 4):

                    os.system('cls')

                    def listar_eleitores(conn):
                        cursor = conn.cursor()
                        
                        input("\nPressione ENTER para listar todos os eleitores.")
                        sql = "SELECT * FROM eleitores"
                        cursor.execute(sql)
                        result = cursor.fetchall()

                        print("Lista de eleitores:")
                        print('-' * 150)
                        for eleitor in result:
                            cpf_A = str(eleitor[4])
                            chaveA = str(eleitor[1])
                            cpf_descriptografado = (descriptografia(cpf_A))
                            chave_descriptografada = (descriptografia(chaveA))
                            print(f"Nome Completo: {eleitor[2]} | Chave de Acesso: {chave_descriptografada} | Título de Eleitor: {eleitor[3]} | CPF Criptografado: {cpf_descriptografado} | Mesário: {eleitor[5]} | Status do Voto: {eleitor[6]}")
                        print('-' * 150)

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
