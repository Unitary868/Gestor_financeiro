from utils import gerar_id_conta

contas = {}

# Atributos da entidade Conta:
#   id      → identificador único
#   nome    → nome do utilizador
#   nif     → número de identificação fiscal
#   pin     → código de autenticação
#   token   → identificador de sessão


# ── Helpers internos ──────────────────────────────────────────

def _validar_nif(nif):
    return nif.isdigit() and len(nif) == 9

def _validar_pin(pin):
    return pin.isdigit() and len(pin) == 4


# ── CREATE ────────────────────────────────────────────────────

def criar_conta(nome, nif, pin):
    if len(nome.strip()) < 2:
        return 400, "Nome deve ter pelo menos 2 caracteres."
    if not _validar_nif(nif):
        return 400, "NIF inválido. Deve ter 9 dígitos."
    if not _validar_pin(pin):
        return 400, "PIN inválido. Deve ter 4 dígitos."

    # Verificar NIF duplicado
    for conta in contas.values():
        if conta["nif"] == nif:
            return 409, "Já existe uma conta com este NIF."

    id_conta = gerar_id_conta()

    conta = {
        "id":    id_conta,
        "nome":  nome.strip(),
        "nif":   nif,
        "pin":   pin,
        "token": f"USR-{id_conta}-ABC123",
    }

    contas[id_conta] = conta
    return 201, conta


# ── READ (listar todas) ───────────────────────────────────────

def listar_contas():
    if not contas:
        return 404, "Não existem contas registadas."
    return 200, contas


# ── READ (consultar individual) ───────────────────────────────

def consultar_conta(id_conta):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    return 200, contas[id_conta]


# ── UPDATE PIN ────────────────────────────────────────────────

def atualizar_pin(id_conta, pin_atual, pin_novo):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin_atual:
        return 401, "PIN atual incorreto."
    if not _validar_pin(pin_novo):
        return 400, "Novo PIN inválido. Deve ter 4 dígitos."

    contas[id_conta]["pin"] = pin_novo
    return 200, contas[id_conta]


# ── DELETE ────────────────────────────────────────────────────

def eliminar_conta(id_conta, pin):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."

    del contas[id_conta]
    return 200, id_conta


# ── AUTH ──────────────────────────────────────────────────────

def verificar_login(id_conta, pin):
    if id_conta not in contas:
        return 404, "Conta não encontrada."
    if contas[id_conta]["pin"] != pin:
        return 401, "PIN incorreto."
    return 200, contas[id_conta]


# ── HELPERS para o main ───────────────────────────────────────

def _resolver_id(id_conta=None):
    """Devolve o id a usar: o fornecido ou o primeiro existente."""
    if not contas:
        return None
    return id_conta if id_conta in contas else next(iter(contas))

def get_nome(id_conta=None):
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, contas[uid]["nome"]

def get_id(id_conta=None):
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, uid

def get_dados(id_conta=None):
    uid = _resolver_id(id_conta)
    if uid is None:
        return 404, "Nenhuma conta encontrada."
    return 200, contas[uid]

def conta_existe():
    return bool(contas)
