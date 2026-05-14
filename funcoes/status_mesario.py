from funcoes.zerezima import zerezima
from funcoes.log_ocorrencia import registrar_log
status_mesario = 0

def abrirMesario(conn):
    global status_mesario
    status_mesario = 1
    zerezima(conn)

    print("A urna foi aberta.")
    registrar_log("ABERTURA", "Votação iniciada com sucesso. Total de votos zerados.") # Registra no log a abertura da urna

def fecharMesario():
    global status_mesario
    status_mesario = 0

    print("A urna foi fechada.")
    registrar_log("ENCERRAMENTO", "Votação finalizada com sucesso.") # Registra no log o encerramento da urna


def status_global():

    if status_mesario == 0:
        return 0

    elif status_mesario == 1:
        return 1