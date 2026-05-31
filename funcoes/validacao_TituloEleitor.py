def validar_titulo_eleitor(titulo):
    """
    Esta função faz a validação um número de título de eleitor de acordo com suas regras de formação, retornando se ele é válido ou não.

    Args:
        titulo (str): Número do título eleitoral a ser validado.

    Returns:
        bool: True se o título for válido, caso contrário False.
    """
    titulo = titulo.strip() #remove espaços em branco no começo e no final da string. para nao ultrapassar os 12 digitos

    # Verifica se tem 12 dígitos e se é número
    if len(titulo) != 12 or not titulo.isdigit():  #verifica se tem 12 digitos e se é tudo número, se não for, retorna false
        return False

    # Separando partes
    numero = titulo[:8] #pega indice do 0 ao 7
    uf = titulo[8:10] #8 ao 9
    dv_informado = titulo[10:] #10 ate o final

    # 1º Dígito Verificador
    soma1 = 0
    peso = 2

    for digito in numero:
        soma1 += int(digito) * peso
        peso += 1

    resto1 = soma1 % 11

    if resto1 == 10:
        dv1 = 0
    else:
        dv1 = resto1

    # 2º Dígito Verificador
    soma2 = (int(uf[0]) * 7) + (int(uf[1]) * 8) + (dv1 * 9)

    resto2 = soma2 % 11

    if resto2 == 10:
        dv2 = 0
    else:
        dv2 = resto2

    dv_calculado = str(dv1) + str(dv2)

    # Comparação final
    if dv_calculado == dv_informado:
        return True
    else:
        return False

def verificarTituloDeEleitorDuplicado(conn, tituloDeEleitor):
    """
    Esta função verifica se um titulo de eleitor já está ou não cadastrado no banco de dados.

    Args:
        conn (mysql.connector): Conexão ativa com o banco de dados MySQL.
        tituloDeEleitor (str): Número do título eleitoral a ser verificado.

    Returns:
        bool: True se o título já foi cadastrado, caso contrário False.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE titulo_eleitor = %s", (tituloDeEleitor,))
    if cursor.fetchone()[0] > 0:
        print("\nTítulo de eleitor ja cadastrado")
        input("Pressione ENTER para voltar.")
        return True
    else:
        return False