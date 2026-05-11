import os
import menu.menu_principal as menu
import funcoes.ascii as ascii
import funcoes.status_mesario as statusMesario
from funcoes.criptografia import criptografia
from sistema.voto import login
from sistema.voto import verificar_voto
from sistema.voto import adicionar_voto
from funcoes.validacaoCPF import validar_cpf, limpar_cpf
import funcoes.resultado as resultado
from funcoes import registrar_log

def votacao(conn):
    os.system('cls')
    ascii.votacaoASCII()
    
    if statusMesario.status_global() == 0:

        print('''
            Digite o valor da opção desejada:

            1. Menu da Urna
            2. Resultados
            3. Auditoria
            4. Voltar
        ''')
        try:
            n = int(input("-> "))
        
            if (n == 1):
                def menu_urna(conn):
                    os.system('cls')
                    print('''
                            Menu da Urna

                            1. Status da Urna
                            2. Gerenciar Urna
                            3. Voltar
                    
                        ''')

                    n = int(input("-> "))
                    try:

                        if (n == 1):

                            os.system('cls')
                            print("\nA urna está fechada.")

                            input("Pressione ENTER para voltar.")
                            return menu_urna(conn)

                        elif (n == 2):
                            os.system('cls')
                            while not verificarMesario(conn):
                                registrar_log("ALERTA", "Tentativa de acesso negado")
                                print("CPF, Chave de acesso ou Título inválidos. Tente novamente.")
                                input("Pressione ENTER para voltar")
                                return votacao(conn)                  
                            os.system('cls')
                            print('''

                                Escolha uma das seguintes opções
                                
                                1. Abrir urna
                                2. Voltar

                            ''')

                            n = int(input("-> "))

                            try:
                                
                                if (n == 1):

                                    os.system('cls')
                                    statusMesario.abrirMesario(conn)

                                    registrar_log( 
                                         "ABERTURA",        
                                         "Votação iniciada com sucesso. Total de votos zerado.")
                                    input("Pressione ENTER para voltar.")
                                    return votacao(conn)

                                elif (n == 2):
                                    return menu_urna(conn)


                                else:
                                    print("Opção inválida. Tente novamente.")
                                    input("\nPressione ENTER para continuar.")
                                    return menu_urna(conn)

                            except ValueError:
                                print("Opção inválida. Tente novamente")

                        elif (n == 3):
                            return votacao(conn)

                        else:
                            print("\nOpção inválida. Tente novamente.")
                            input("\nPressione ENTER para continuar.")
                            return menu_urna(conn)

                    except ValueError:
                        print("\nOpção inválida. Tente novamente.")
                        return menu_urna(conn)
                menu_urna(conn)
            
            elif (n == 2):
                def resultados_votacao(conn):
                    os.system('cls')
                    n = 0
                    while n!= 1 and n!= 2 and n!= 3 and n!= 4:
                        print('''
                        Resultados

                        1. Boletim de Urna
                        2. Estatísticas
                        3. Votos por Partido
                        4. Validação de Integridade
                        5. Voltar
                        ''')
                        n = int(input("-> "))
                        if n!= 1 and n!= 2 and n!= 3 and n!= 4 and n!= 5:
                            print("Opção inválida. Tente novamente.")

                        elif (n == 1):
                            resultado.boletim_urna(conn)
                            input("\nPressione ENTER para voltar.")
                            return votacao(conn)

                        elif (n == 2):
                            resultado.estatistica_comparecimento(conn)  
                            input("\nPressione ENTER para voltar.")
                            return votacao(conn)

                        elif (n == 3):
                            resultado.votos_por_partido(conn)
                            input("\nPressione ENTER para voltar.")
                            return votacao(conn)

                        elif (n == 4):
                            resultado.validacao_integridade(conn)
                            input("\nPressione ENTER para voltar.")
                            return votacao(conn)

                        elif (n == 5):
                            os.system('cls')
                            return votacao(conn)

                resultados_votacao(conn)

            elif (n == 3):
                def auditoria_votacao(conn):
                    os.system('cls')
                    n = 0
                    while n!= 1 and n!= 2 and n!= 3:
                        print('''
                        Auditoria

                        1. Ver Logs
                        2. Ver Protocolos
                        3. Voltar
                        ''')
                        n = int(input("-> "))
                        if n!= 1 and n!= 2 and n!= 3:
                            print("Opção inválida. Tente novamente.")

                        elif (n == 1):
                            print('Em produção...')

                        elif (n == 2):
                            print('Em produção...')

                        elif (n == 3):
                            os.system('cls')
                            return votacao(conn)

                auditoria_votacao(conn)
            
            elif (n == 4):
                os.system('cls')
                return menu.menu(conn)
                
            else:
                print("Opção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar.")
                return votacao(conn)  
            
        except ValueError:
            print("Opção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar.")
            return votacao(conn)
        
    elif statusMesario.status_global() == 1:

        print('''
            Digite o valor da opção desejada:

            1. Menu da Urna
            2. Auditoria
            3. Voltar
        ''')
        try:
            n = int(input("-> "))
        
            
            if (n == 1):
                def menu_urna(conn):
                    os.system('cls')

                    print('''
                            Menu da Urna

                            1. Votar
                            2. Status da Urna
                            3. Gerenciar Urna
                            4. Voltar
                    
                        ''')

                    n = int(input("-> "))
                    try:
                        
                        if (n == 1):
                                id_eleitor = login(conn) # Guardando o valor de retorno da função login
                                status_voto = verificar_voto(id_eleitor, conn) #Guardando o valor de retorno da função verificar_voto e utilizando o parâmetro da variável acima
                                if status_voto == 1: # Verifica se o status de voto do eleitor é igual a 1
                                    registrar_log("ALERTA", "Eleitor tentou votar novamente") # Registra no log a tentativa de voto novamente
                                    print("Você ja votou!")
                                    input("Pressione ENTER para voltar.")
                                    return menu_urna(conn)
                                else:
                                    adicionar_voto(id_eleitor, conn) # Puxa a função adicionar_voto com o parâmetro do id do eleitor

                                input("Pressione ENTER para voltar.")
                                return menu_urna(conn)

                        elif (n == 2):

                            os.system('cls')

                            print("\nA urna está aberta.")

                            input("Pressione ENTER para voltar.")

                            return menu_urna(conn)

                        elif (n == 3):
                            os.system('cls')
                            while not verificarMesario(conn):
                                registrar_log("ALERTA", "Tentativa de acesso negado")
                                print("CPF, Chave de acesso ou Título inválidos. Tente novamente.")
                                input("Pressione ENTER para voltar")
                                return votacao(conn)                  
                            os.system('cls')
                            print('''

                                Escolha uma das seguintes opções
                                
                                1. Fechar urna
                                2. Voltar

                            ''')

                            n = int(input("-> "))

                            try:
                                
                                if (n == 1):

                                    os.system('cls')
                                    statusMesario.fecharMesario()
                                    input("Pressione ENTER para voltar.")
                                    return votacao(conn)

                                elif (n == 2):
                                    return menu_urna(conn)


                                else:
                                    print("Opção inválida. Tente novamente.")
                                    input("\nPressione ENTER para continuar.")
                                    return menu_urna(conn)

                            except ValueError:
                                print("Opção inválida. Tente novamente")

                        elif (n == 4):
                            return votacao(conn)

                        else:
                            print("\nOpção inválida. Tente novamente.")
                            input("\nPressione ENTER para continuar.")
                            return menu_urna(conn)

                    except ValueError:
                        print("\nOpção inválida. Tente novamente.")
                return menu_urna(conn)

            elif (n == 2):
                def auditoria_votacao(conn):
                    os.system('cls')
                    n = 0
                    while n!= 1 and n!= 2 and n!= 3:
                        print('''
                        Auditoria

                        1. Ver Logs
                        2. Ver Protocolos
                        3. Voltar
                        ''')
                        n = int(input("-> "))
                        if n!= 1 and n!= 2 and n!= 3:
                            print("Opção inválida. Tente novamente.")

                        elif (n == 1):
                            print('Em produção...')

                        elif (n == 2):
                            print('Em produção...')

                        elif (n == 3):
                            os.system('cls')
                            return votacao(conn)

                auditoria_votacao(conn)
            
            elif (n == 3):
                os.system('cls')
                return menu.menu(conn)
                
            else:
                print("Opção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar.")
                return votacao(conn)  
            
        except ValueError:
            print("Opção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar.")
            return votacao(conn)

def verificarMesario(conn):
    ascii.mesarioASCII()

    cpf_crip = str(input("Digite seu CPF: "))
    while not validar_cpf(cpf_crip):
                registrar_log("ALERTA", "Tentativa de acesso negado") # Registra no log a tentativa de acesso negado
                print("CPF inválido. Tente novamente.")
                cpf_crip = str(input("Digite seu CPF: "))
    cpf_crip = limpar_cpf(cpf_crip)
    cpf_crip = criptografia(cpf_crip) # Criptografa o cpf

    titulo = str(input("Digite seu título de eleitor: "))

    chaveDeAcesso = input('Digite a chave de acesso do mesário: ')
    chaveDeAcesso_Criptografada = criptografia(chaveDeAcesso)
    
    cursor = conn.cursor()
    cursor.execute('SELECT mesario FROM eleitores WHERE chave_acesso = %s AND cpf_criptografado = %s AND titulo_eleitor = %s', (chaveDeAcesso_Criptografada, cpf_crip, titulo))
    resultado = cursor.fetchone()
    cursor.close() 
    
    return resultado[0] if resultado else None