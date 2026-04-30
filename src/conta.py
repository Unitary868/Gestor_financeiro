# ==============================
# conta.py
# CRUD simples para entidade Conta
# SEM utilização de classes
# armazenamento em dicionario
# validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_conta

contas = {}  # ← AGORA VÁRIAS CONTAS!


# CREATE
def criar_conta(nome, nif, pin, saldo_inicial):
    # Validações AQUI (como o prof)
    if len(nome.strip()) < 2:
        return 400, "Nome deve ter pelo menos 2 caracteres"
    if not (nif.isdigit() and len(nif) == 9):
        return 400, "NIF inválido. Deve ter 9 dígitos"
    if not (pin.isdigit() and len(pin) == 4):
        return 400, "PIN inválido. Deve ter 4 dígitos"
    if saldo_inicial < 0:
        return 400, "Saldo inicial não pode ser negativo"

    id_conta = gerar_id_conta()

    conta = {
        "nome": nome.strip(),
        "nif": nif,
        "pin": pin,
        "saldo": saldo_inicial,
        "token": f"USR-{id_conta}-ABC123"  # simplificado
    }

    contas[id_conta] = conta
    return 201, conta


# READ (listar todas)
def listar_contas():
    if not contas:
        return 404, "Não existem contas registadas."
    return 200, contas


# READ (consultar individual)
def consultar_conta(id_conta):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    return 200, contas[id_conta]


# UPDATE PIN
def atualizar_pin(id_conta, pin_atual, pin_novo):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin_atual:
        return 401, "PIN atual incorreto."
    if not (pin_novo.isdigit() and len(pin_novo) == 4):
        return 400, "Novo PIN inválido. Deve ter 4 dígitos"

    contas[id_conta]["pin"] = pin_novo
    return 200, contas[id_conta]


# DELETE
def eliminar_conta(id_conta, pin):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."

    del contas[id_conta]
    return 200, id_conta


# HELPERS para o main (como get_nome, get_id do teu main)
def get_nome(id_conta=None):
    if not contas:
        return 404, "Nenhuma conta encontrada."
    # Pega a primeira (ou a logada)
    uid = id_conta or next(iter(contas))
    return 200, contas[uid]["nome"]


def get_id(id_conta=None):
    if not contas:
        return 404, "Nenhuma conta encontrada."
    uid = id_conta or next(iter(contas))
    return 200, uid


def get_dados(id_conta=None):
    if not contas:
        return 404, "Nenhuma conta encontrada."
    uid = id_conta or next(iter(contas))
    return 200, contas[uid]


def verificar_login(id_conta, pin):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."
    return 200, contas[id_conta]


def conta_existe():
    return 200, bool(contas)