# ==============================
# conta.py
# CRUD simples para entidade Conta
# SEM utilização de classes
# Armazenamento em dicionário
# Validações feitas aqui (não no main)
# ==============================

import json
import os
from utils import gerar_id_conta, gerar_token

contas = {}

FICHEIRO_CONTAS = "contas.json"

# Atributos da entidade Conta:
#   id      → identificador único
#   nome    → nome do utilizador
#   nif     → número de identificação fiscal
#   pin     → código de autenticação
#   token   → identificador de sessão


# ── Persistência ──────────────────────────────────────────────

def guardar_contas():
    with open(FICHEIRO_CONTAS, "w", encoding="utf-8") as ficheiro:
        json.dump(contas, ficheiro, indent=4, ensure_ascii=False)

def carregar_contas():
    global contas
    if os.path.exists(FICHEIRO_CONTAS):
        with open(FICHEIRO_CONTAS, "r", encoding="utf-8") as ficheiro:
            contas = json.load(ficheiro)
    else:
        contas = {}


# ── Helpers internos ──────────────────────────────────────────

def _validar_nif(nif):
    return nif.isdigit() and len(nif) == 9

def _validar_pin(pin):
    return pin.isdigit() and len(pin) == 4

def _gerar_id_unico():
    novo = gerar_id_conta()
    while novo in contas:
        novo = gerar_id_conta()
    return novo


# ── CREATE ────────────────────────────────────────────────────

def criar_conta(nome, nif, pin):
    carregar_contas()

    if len(nome.strip()) < 2:
        return 400, "Nome deve ter pelo menos 2 caracteres."
    if not _validar_nif(nif):
        return 400, "NIF inválido. Deve ter 9 dígitos."
    if not _validar_pin(pin):
        return 400, "PIN inválido. Deve ter 4 dígitos."

    for conta in contas.values():
        if conta["nif"] == nif:
            return 409, "Já existe uma conta com este NIF."

    id_conta = _gerar_id_unico()

    conta = {
        "id":    id_conta,
        "nome":  nome.strip(),
        "nif":   nif,
        "pin":   pin,
        "token": gerar_token(id_conta),
    }

    contas[id_conta] = conta
    guardar_contas()
    return 201, conta


# ── READ (listar todas) ───────────────────────────────────────

def listar_contas():
    carregar_contas()

    if not contas:
        return 404, "Não existem contas registadas."
    return 200, contas


# ── READ (consultar individual) ───────────────────────────────

def consultar_conta(id_conta):
    carregar_contas()

    if id_conta not in contas:
        return 404, "Conta não encontrada."
    return 200, contas[id_conta]


# ── UPDATE PIN ────────────────────────────────────────────────

def atualizar_pin(id_conta, pin_atual, pin_novo):
    carregar_contas()

    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin_atual:
        return 401, "PIN atual incorreto."
    if not _validar_pin(pin_novo):
        return 400, "Novo PIN inválido. Deve ter 4 dígitos."

    contas[id_conta]["pin"] = pin_novo
    guardar_contas()
    return 200, contas[id_conta]


# ── DELETE ────────────────────────────────────────────────────

def eliminar_conta(id_conta, pin):
    carregar_contas()

    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."

    del contas[id_conta]
    guardar_contas()
    return 200, id_conta


# ── AUTH ──────────────────────────────────────────────────────

def verificar_login(id_conta, pin):
    carregar_contas()

    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."
    return 200, contas[id_conta]


# ── HELPERS para o main ───────────────────────────────────────

def _resolver_id(id_conta=None):
    if not contas:
        return None
    return id_conta if id_conta in contas else next(iter(contas))

def get_nome(id_conta=None):
    carregar_contas()
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, contas[uid]["nome"]

def get_id(id_conta=None):
    carregar_contas()
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, uid

def get_dados(id_conta=None):
    carregar_contas()
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, contas[uid]

def conta_existe():
    carregar_contas()
    return bool(contas)
