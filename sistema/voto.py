import os
import random
import string
from funcoes import ascii
from funcoes.criptografia import criptografia
from funcoes.descriptografia import descriptografia
from funcoes.validacaoCPF import validar_cpf, limpar_cpf, primeiros_quatro_digitos
import mysql.connector
from datetime import datetime
from funcoes import registrar_log   


'''
    menu -> votacao - > voto.py
    aqui tem que implementar a parte de votar
    pedir pro eleitor realizar o login 
    validar no banco a senha, ver se ja votou, cpf e valido...
'''

def login(conn):
    try:
        os.system('cls')
        ascii.votacaoASCII()
        cursor = conn.cursor() # Cria um cursor pra fazer as mudanças

        cpf = str(input("Digite os 4 primeiros dígitos do CPF: "))
        while not cpf.isdigit() or len(cpf) != 4:
            registrar_log("ALERTA", "Tentativa de acesso negado")
            print("Digite exatamente 4 números.")
            cpf = input("Digite os 4 primeiros dígitos do CPF: ")
        cpf = limpar_cpf(cpf)

        titulo = str(input("Digite seu título de eleitor: "))

        chave = str(input("Digite a chave de acesso: "))
        chave = criptografia(chave) # Criptografa a chave

        cursor.execute('''
            SELECT id, cpf_criptografado FROM eleitores 
            WHERE chave_acesso = %s AND titulo_eleitor = %s
            ''', (chave, titulo))

        resultado = cursor.fetchall() # Guarda o resultado do cursor em uma variável

        for eleitor in resultado:
            cpf_descriptografado = descriptografia(eleitor[1])
            if primeiros_quatro_digitos(cpf_descriptografado) == cpf:
                return eleitor[0]  # id do eleitor
           
        print("CPF, TÍTULO ou CHAVE inválidos. Tente novamente.") # Se retornar nada, significa que o CPF, TÍTULO ou CHAVE estão invalidas
        registrar_log("ALERTA", "Tentativa de acesso negado") # Registra no log a tentativa de acesso negado
        return login(conn) # Retorna pra função novamente

    except ValueError:
        print("Erro. Tente novamente.")
        return login(conn) # Em caso de erro, retorna pra função novamente
    
    finally: # Quando tudo acima terminar
        cursor.close() # Fecha o cursor

def verificar_voto(eleitor_id, conn): # Criação de uma função com um parâmetro

    try:
        cursor = conn.cursor() # Criação do cursor para modificação do banco

        cursor.execute('''
            SELECT status_voto FROM eleitores WHERE id = %s
                       ''',(eleitor_id,)) # Seleciona o status do voto do eleitor em base de seu id
        
        voto_status = cursor.fetchone()[0] # Extrai o valor que está dentro da tupla para dentro da variável voto_status

        return voto_status # Retorna o status do voto

    except  mysql.connector.Error as e: # Tratando erros 
        print(f"Erro no banco: {e}")
                        
    finally: # Quando tudo acima tiver feito fecha o cursor e a conexão com o banco
        cursor.close()

def adicionar_voto(eleitor_id, conn): # Criação de uma função com um parâmetro do id do eleitor

    try:
        cursor = conn.cursor() # Cria um cursor para modificação no banco
        id_candidato = None

        while not id_candidato:
            os.system('cls')
            ascii.votacaoASCII()
            voto = int(input("Digite o número de seu candidato: "))
            cursor.execute('''
                SELECT id FROM candidatos WHERE numero_votacao = %s
                        ''', (voto,)) # Seleciona o id do candidato em base do seu numero de voto
            id_candidato = cursor.fetchone() # Atribui ao id_candidato a tupla 
            os.system('cls')

            if id_candidato: # Se a tupla id_candidato existir, ou seja, se o número do candidato for válido, extrai o valor do id do candidato da tupla e atribui à variável id_candidato
                id_candidato = id_candidato[0] # Extrai o valor id do candidato da tupla
            else:
                ascii.votacaoASCII()
                input("Candidato inválido.")
                continue

        sql = 'SELECT nome_completo, numero_votacao, nome_partido, foto_ascii FROM candidatos WHERE numero_votacao = %s'
        cursor.execute(sql,(voto,))

        resultado = cursor.fetchone()
        if resultado:
            if resultado[3]:
                try:
                    with open(resultado[3], 'r', encoding='utf-8') as f:
                        print(f.read())
                except:
                    print('Erro ao carregar ASCII')
            else:
                print('Sem Imagem')
            print(f"Nome: {resultado[0]}")
            print(f"Número: {resultado[1]}")
            print(f"Partido: {resultado[2]}")

        n = str(input("Deseja confirmar seu voto no seguinte candidato? (S/N) -> ")).lower()

        while n != "s" and n != "n":
            print("Digite apenas 's' ou 'n'")
            n = input("Deseja confirmar seu voto? (S/N) -> ").lower()

        if (n == "s"):
            data_atual = datetime.now() # Pega a data atual

            #Criação do protocolo de votação
            letra1 = random.choice(string.ascii_uppercase) # Gera uma letra maiúscula aleatória
            letra2 = random.choice(string.ascii_uppercase) # Gera uma letra maiúscula aleatória
            num1 = random.choice (string.digits) # Gera um número aleatório
            num2 = random.choice (string.digits) # Gera um número aleatório
            num3 = random.choice (string.digits) # Gera um número aleatório
            num4 = random.choice (string.digits) # Gera um número aleatório
            num5 = random.choice (string.digits) # Gera um número aleatório

            ano = "26" # Define o ano como 2026
            numero_candidato = str(voto) # Converte o número do candidato para string   

            protocolo = (
                "V" +
                letra1 +
                letra2 +
                ano +
                numero_candidato +
                num1 +
                num2 +
                num3 +
                num4 +
                num5
                    ) # Cria o protocolo de votação juntando as partes  
            
            protocolo_criptografado = criptografia(protocolo)
            
            cursor.execute('''
                INSERT into tabela_votos (id_candidato, data_hora_voto, protocolo_criptografado)
                VALUES (%s, %s, %s)
                        ''', (id_candidato, data_atual, protocolo_criptografado)) # Insere no banco as informações de votação
            
            conn.commit() # Comita tudo

            print("Voto registrado com sucesso!")
            print("Protocolo de votação:", protocolo) # Mostra o protocolo de votação para o eleitor
            registrar_log("SUCESSO", f"Eleitor com ID {eleitor_id} votou com o protocolo {protocolo}") # Registra no log o sucesso do voto

            cursor.execute('''
                UPDATE eleitores SET status_voto = %s WHERE id = %s
                        ''', (1, eleitor_id)) # Da update no status do eleitor
            conn.commit() # Comita

        elif (n == "n"):
            os.system('cls')
            ascii.votacaoASCII()
            n = input("Seu voto não será computado. Pressione ENTER para voltar.")
            return adicionar_voto(eleitor_id, conn)
        
    except mysql.connector.IntegrityError as e:
        print(f"\nErro ao votar: {e}") # Mostrando algum erro

    finally:
        cursor.close() # Fecha o cursor
