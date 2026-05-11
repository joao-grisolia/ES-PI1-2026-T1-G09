from datetime import datetime

# -- Registra um evento no arquivo de log de ocorrência.
#
#       A função necessita que sejam passado dois parâmetros nela:
#           - Tipo do evento (string): Registra o tipo do evento (ABERTURA, ENCERRAMENTO, ALERTA, SUCESSO ... etc)
#           - Mensagem (string): Registra a descrição do log de evento ocorrido

def registrar_log(tipo_evento,mensagem):

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha_terminal = f"[{data_hora}] {tipo_evento}: {mensagem}\n"

    with open("log_ocorrencias.txt", "a", encoding="utf-8") as arq:
        arq.write(linha_terminal)

# -- Exibe todos os logs que ocorreram durante o processo de eleição.
#       
#       O loop tenta ler o arquivo log_ocorrencias.txt, se houver algum log sequer, a função printa ela,
#       se não houver, printa erro.

def exibir_logs():

    try:
        with open("log_ocorrencias.txt","r", encoding="utf-8") as arq:
            print(arq.read())
    
    except FileNotFoundError:
        print("Nenhum log encontrado. Tente novamente.")