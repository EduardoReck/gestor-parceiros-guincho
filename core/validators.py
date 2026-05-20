import re


def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    d1 = calcular_digito(cnpj, pesos1)
    d2 = calcular_digito(cnpj, pesos2)

    return int(cnpj[12]) == d1 and int(cnpj[13]) == d2


def validar_email(email):
    if not email:
        return True
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email))


def validar_telefone(telefone):
    if not telefone:
        return True
    digits = re.sub(r'\D', '', telefone)
    return 10 <= len(digits) <= 11


def formatar_cnpj(texto):
    digits = re.sub(r'\D', '', texto)[:14]
    n = len(digits)
    if n <= 2:  return digits
    if n <= 5:  return f"{digits[:2]}.{digits[2:]}"
    if n <= 8:  return f"{digits[:2]}.{digits[2:5]}.{digits[5:]}"
    if n <= 12: return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:]}"
    return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"


def formatar_telefone(texto):
    digits = re.sub(r'\D', '', texto)[:11]
    n = len(digits)
    if n == 0:  return ""
    if n <= 2:  return f"({digits}"
    if n <= 6:  return f"({digits[:2]}) {digits[2:]}"
    if n <= 10: return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"


def formatar_cep(texto):
    digits = re.sub(r'\D', '', texto)[:8]
    if len(digits) <= 5:
        return digits
    return f"{digits[:5]}-{digits[5:]}"
