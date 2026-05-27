import os
import menu.menu_principal as menu
import funcoes.ascii as ascii
import funcoes.status_mesario as statusMesario
from funcoes.criptografia import criptografia
from sistema.voto import login
from sistema.voto import verificar_voto
from sistema.voto import adicionar_voto
import funcoes.resultado as resultado
from funcoes.log_ocorrencia import registrar_log, exibir_logs
from funcoes.descriptografia import descriptografia

def votacao(conn):
    os.system('cls')
    ascii.votacaoASCII()
    
    # MENU URNA FECHADA
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
                menu_urnaFechada(conn)
            elif (n == 2):
                resultados_votacao(conn)
            elif (n == 3):
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
    
    # MENU URNA ABERTA
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
                return menu_urnaAberta(conn)
            elif (n == 2):
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

def menu_urnaFechada(conn):
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
            return menu_urnaFechada(conn)

        elif (n == 2):
            os.system('cls')
            ascii.mesarioASCII()
            while not login(conn):
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
                    return menu_urnaFechada(conn)


                else:
                    print("Opção inválida. Tente novamente.")
                    input("\nPressione ENTER para continuar.")
                    return menu_urnaFechada(conn)

            except ValueError:
                print("Opção inválida. Tente novamente")

        elif (n == 3):
            return votacao(conn)

        else:
            print("\nOpção inválida. Tente novamente.")
            input("\nPressione ENTER para continuar.")
            return menu_urnaFechada(conn)

    except ValueError:
        print("\nOpção inválida. Tente novamente.")
        return menu_urnaFechada(conn)

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
            os.system('cls')
        
            exibir_logs()
            
            input("\nPressione ENTER para voltar.")
            return auditoria_votacao(conn)

        elif (n == 2):
            os.system('cls')
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT protocolo_criptografado FROM tabela_votos')
                protocolos = cursor.fetchall()
                cursor.close()

                if protocolos:
                    print("Protocolos:")
                    print("-" * 50)
                    for protocolo in protocolos:
                        print(f"- {descriptografia(protocolo[0])}")
                    print("-" * 50)
                    print(f"Total de protocolos: {len(protocolos)}")
                else:
                    print("Nenhum protocolo encontrado")

            except Exception as e:
                print(f"Erro ao consultar protocolos: {e}")

            input("\nPressione ENTER para voltar.")
            return auditoria_votacao(conn)

        elif (n == 3):
            os.system('cls')
            return votacao(conn)

def menu_urnaAberta(conn):
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
                    os.system('cls')
                    ascii.votacaoASCII()
                    id_eleitor = login(conn) # Guardando o valor de retorno da função login
                    while not id_eleitor:
                        print("CPF, TÍTULO ou CHAVE inválidos. Tente novamente.")
                        registrar_log("ALERTA", "Tentativa de acesso negado")
                        input("Aperte ENTER para tentar novamente.")
                        os.system('cls')
                        ascii.votacaoASCII()
                        id_eleitor = login(conn)
                    status_voto = verificar_voto(id_eleitor, conn) #Guardando o valor de retorno da função verificar_voto e utilizando o parâmetro da variável acima
                    if status_voto == 1: # Verifica se o status de voto do eleitor é igual a 1
                        registrar_log("ALERTA", "Tentativa de voto duplo") # Registra no log a tentativa de voto novamente
                        print("Você ja votou!")
                        input("Pressione ENTER para voltar.")
                        return menu_urnaAberta(conn)
                    else:
                        adicionar_voto(id_eleitor, conn) # Puxa a função adicionar_voto com o parâmetro do id do eleitor

                    input("Pressione ENTER para voltar.")
                    return menu_urnaAberta(conn)

            elif (n == 2):

                os.system('cls')

                print("\nA urna está aberta.")

                input("Pressione ENTER para voltar.")

                return menu_urnaAberta(conn)

            elif (n == 3):
                os.system('cls')
                ascii.mesarioASCII()
                while not login(conn):
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
                        confirmacao = input("Tem certeza que deseja fechar a urna? (s/n): ")
                        if confirmacao.lower() == 'n':
                            print("Encerramento da urna cancelado!")
                            input("Pressione ENTER para voltar.")
                            return menu_urnaAberta(conn)
                        
                        elif confirmacao.lower() == 's':
                            print("Dupla confirmação: Digite novamente sua chave de acesso para fechar a urna.")
                            if ConfirmarChaveMesario(conn):
                                statusMesario.fecharMesario()
                                registrar_log("ENCERRAMENTO", "Votação finalizada com sucesso.")
                                input("Pressione ENTER para voltar.")
                                return votacao(conn)
                            else:
                                registrar_log("ALERTA", "Tentativa de acesso negado")
                                print("Chave de acesso invalida! Tente novamente.")
                                input("Pressione ENTER para voltar")
                                return menu_urnaAberta(conn)
                        else:
                            print("Opção inválida. Retornando ao menu da urna.")
                            input("Pressione ENTER para continuar.")
                            return menu_urnaAberta(conn)
                        
                    elif (n == 2):
                        return menu_urnaAberta(conn)


                    else:
                        print("Opção inválida. Tente novamente.")
                        input("\nPressione ENTER para continuar.")
                        return menu_urnaAberta(conn)

                except ValueError:
                    print("Opção inválida. Tente novamente")

            elif (n == 4):
                return votacao(conn)

            else:
                print("\nOpção inválida. Tente novamente.")
                input("\nPressione ENTER para continuar.")
                return menu_urnaAberta(conn)

        except ValueError:
            print("\nOpção inválida. Tente novamente.")

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
            os.system('cls')
            try:
                exibir_logs()

            except Exception as e:
                print(f"Erro ao exibir logs: {e}")
                
            input("\nPressione ENTER para voltar.")
            return auditoria_votacao(conn)

        elif (n == 2):
            os.system('cls')
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT protocolo_criptografado FROM tabela_votos')
                protocolos = cursor.fetchall()
                cursor.close()

                if protocolos:
                    print("Protocolos:")
                    print("-" * 50)
                    for protocolo in protocolos:
                        print(f"- {descriptografia(protocolo[0])}")
                    print("-" * 50)
                    print(f"Total de protocolos: {len(protocolos)}")
                else:
                    print("Nenhum protocolo encontrado")

            except Exception as e:
                print(f"Erro ao consultar protocolos: {e}")

            input("\nPressione ENTER para voltar.")
            return auditoria_votacao(conn)

        elif (n == 3):
            os.system('cls')
            return votacao(conn)

def ConfirmarChaveMesario(conn):
    chave = input("Digite novamente a chave de acesso do mesário: ")
    chave_criptografada = criptografia(chave)

    cursor = conn.cursor()
    cursor.execute('SELECT mesario FROM eleitores WHERE chave_acesso = %s', (chave_criptografada,))

    resultado = cursor.fetchone()
    cursor.close()

    return resultado[0] if resultado else None
