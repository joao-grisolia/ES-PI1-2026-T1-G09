from funcoes.criptografia import criptografia

#---------- Função para se obter os 4 primeiros dígitos do CPF ----------

def primeiros_quatro_digitos(cpf):

    try:
        # Converte para string e remove sinal negativo
        num_str = str(abs(int(cpf)))
        
        # Retorna os primeiros 4 caracteres
        return num_str[:4]

    except ValueError:

        raise ValueError("Entrada inválida. Forneça um número inteiro.")

#------------------------------------------------------------------------
def limpar_cpf(cpf):
    cpf_limpo = ""

    for i in cpf:
        if i.isdigit():
            cpf_limpo += i

    return cpf_limpo

def validar_cpf(cpf):
    cpf_limpo = limpar_cpf(cpf)

    # CPF válido deve ter exatamente 11 dígitos
    if len(cpf_limpo) != 11:
        return False

    # Verifica CPFs inválidos conhecidos (todos os dígitos iguais)
    if (
        cpf_limpo == "00000000000" or
        cpf_limpo == "11111111111" or
        cpf_limpo == "22222222222" or
        cpf_limpo == "33333333333" or
        cpf_limpo == "44444444444" or
        cpf_limpo == "55555555555" or
        cpf_limpo == "66666666666" or
        cpf_limpo == "77777777777" or
        cpf_limpo == "88888888888" or
        cpf_limpo == "99999999999"
    ):
        return False

    # -------- Cálculo do primeiro dígito verificador --------
    soma = 0
    peso = 10
    i = 0

    # Multiplica os 9 primeiros dígitos pelos pesos de 10 a 2
    while i < 9:
        soma += int(cpf_limpo[i]) * peso
        peso -= 1
        i += 1

    # Calcula o resto da divisão por 11
    resto = soma % 11

    # Regra do primeiro dígito verificador
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Verifica se o primeiro dígito calculado confere
    if digito1 != int(cpf_limpo[9]):
        return False

    # -------- Cálculo do segundo dígito verificador --------
    soma = 0
    peso = 11
    i = 0

    # Multiplica os 10 primeiros dígitos pelos pesos de 11 a 2
    while i < 10:
        soma += int(cpf_limpo[i]) * peso
        peso -= 1
        i += 1

    # Calcula o resto da divisão por 11
    resto = soma % 11

    # Regra do segundo dígito verificador
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verifica se o segundo dígito calculado confere
    if digito2 != int(cpf_limpo[10]):
        return False

    # Se passou por todas as validações, o CPF é válido
    return True

def verificarCpfDuplicado(conn ,cpf):
    cursor = conn.cursor()
    cpfCriptografado = criptografia(cpf)
    cursor.execute("SELECT COUNT(*) FROM eleitores WHERE cpf_criptografado = %s", (cpfCriptografado,))
    if cursor.fetchone()[0] > 0:
        print("\nCPF ja cadastrado")
        input("Pressione ENTER para voltar.")
        return True
    else:
        return False