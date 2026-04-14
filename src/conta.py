# conta.py – Entidade Conta

from utils import gerar_id, gerar_token

# ── Dados globais ─────────────────────────────────────────────

conta = {}


# ── CRUD ──────────────────────────────────────────────────────

def criar_conta(nome, nif, pin):
    try:
        if conta:
            return (409, "Já existe uma conta criada.")
        uid = gerar_id()
        token = gerar_token(uid)
        conta["id"] = uid
        conta["nome"] = nome
        conta["nif"] = nif
        conta["pin"] = pin
        conta["token"] = token
        return (201, f"Conta criada com sucesso.\n  ID:    {uid}\n  Token: {token}")
    except Exception as e:
        return (500, str(e))


def conta_existe():
    try:
        return (200, bool(conta))
    except Exception as e:
        return (500, str(e))


def atualizar_pin(uid, pin_atual, pin_novo):
    try:
        status, msg = verificar_login(uid, pin_atual)
        if status != 200:
            return (status, msg)
        conta["pin"] = pin_novo
        return (200, "PIN atualizado com sucesso.")
    except Exception as e:
        return (500, str(e))


def eliminar_conta(uid, pin):
    try:
        status, msg = verificar_login(uid, pin)
        if status != 200:
            return (status, msg)
        conta.clear()
        return (200, "Conta eliminada com sucesso.")
    except Exception as e:
        return (500, str(e))


def verificar_login(uid, pin):
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        if conta.get("id") == uid and conta.get("pin") == pin:
            return (200, "Login bem-sucedido.")
        return (401, "ID ou PIN incorretos.")
    except Exception as e:
        return (500, str(e))


def get_dados():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, {
            "id": conta.get("id", "—"),
            "nome": conta.get("nome", "—"),
            "nif": conta.get("nif", "—"),
            "token": conta.get("token", "—"),
        })
    except Exception as e:
        return (500, str(e))


def get_nome():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("nome", "—"))
    except Exception as e:
        return (500, str(e))


def get_id():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("id", "—"))
    except Exception as e:
        return (500, str(e))


def get_token():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("token", "—"))
    except Exception as e:
        return (500, str(e))