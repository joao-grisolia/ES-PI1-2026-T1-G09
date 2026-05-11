from funcoes.zerezima import zerezima
from funcoes import registrar_log
status_mesario = 0

def abrirMesario(conn):
    global status_mesario
    status_mesario = 1
    zerezima(conn)

    print("A urna foi aberta.")
    registrar_log("ABERTURA", "A urna foi aberta") # Registra no log a abertura da urna

def fecharMesario():
    global status_mesario
    status_mesario = 0

    print("A urna foi fechada.")
    registrar_log("ENCERRAMENTO", "A urna foi fechada") # Registra no log o encerramento da urna


def status_global():

    if status_mesario == 0:
        return 0

    elif status_mesario == 1:
        return 1