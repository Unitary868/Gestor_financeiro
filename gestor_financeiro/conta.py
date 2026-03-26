# conta.py – Entidade Conta

from utils import gerar_id, gerar_token

# ── Dados globais ─────────────────────────────────────────────

conta = {}

# ── CRUD ──────────────────────────────────────────────────────

def criar_conta(nome, nif, pin):
    uid   = gerar_id()
    token = gerar_token(uid)
    conta["id"]    = uid
    conta["nome"]  = nome
    conta["nif"]   = nif
    conta["pin"]   = pin
    conta["token"] = token
    return uid, token

def conta_existe():
    return bool(conta)

def verificar_login(uid, pin):
    return conta.get("id") == uid and conta.get("pin") == pin

def get_nome():  return conta.get("nome",  "—")
def get_id():    return conta.get("id",    "—")
def get_token(): return conta.get("token", "—")
