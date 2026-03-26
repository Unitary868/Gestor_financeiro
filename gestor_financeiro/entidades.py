# entidades.py – Entidades: Transações e Conta

# ── Dados globais ─────────────────────────────────────────────

transacoes = []   # lista de dicionários {id, tipo, descricao, valor, categoria}
conta      = {}   # dicionário com os dados do utilizador
_id_t      = 0    # contador de IDs de transações

CATEGORIAS = (
    "Alimentação", "Transporte", "Lazer",    "Saúde",
    "Educação",    "Habitação",  "Vestuário", "Tecnologia",
    "Poupança",    "Salário",    "Freelance", "Outros",
)

# ── Conta ─────────────────────────────────────────────────────

def criar_conta(nome, nif, pin, uid, token):
    conta["id"] = uid; conta["nome"] = nome
    conta["nif"] = nif; conta["pin"] = pin; conta["token"] = token

def conta_existe():          return bool(conta)
def verificar_login(uid, pin): return conta.get("id") == uid and conta.get("pin") == pin
def get_nome():              return conta.get("nome",  "—")
def get_id():                return conta.get("id",    "—")
def get_token():             return conta.get("token", "—")

# ── Transações – CRUD ─────────────────────────────────────────

def adicionar_transacao(tipo, descricao, valor, categoria):
    global _id_t
    _id_t += 1
    transacoes.append({"id": _id_t, "tipo": tipo,
                        "descricao": descricao, "valor": valor, "categoria": categoria})
    return _id_t

def encontrar_transacao(id_t):
    for i, t in enumerate(transacoes):
        if t["id"] == id_t: return i, t
    return -1, None

def editar_transacao(id_t, desc=None, valor=None, cat=None):
    idx, _ = encontrar_transacao(id_t)
    if idx == -1: return False
    if desc:  transacoes[idx]["descricao"] = desc
    if valor: transacoes[idx]["valor"]     = valor
    if cat:   transacoes[idx]["categoria"] = cat
    return True

def apagar_transacao(id_t):
    idx, _ = encontrar_transacao(id_t)
    if idx == -1: return False
    transacoes.pop(idx); return True

def listar_transacoes(filtro="todas", categoria=None):
    if filtro == "receitas": return [t for t in transacoes if t["tipo"] == "receita"]
    if filtro == "despesas": return [t for t in transacoes if t["tipo"] == "despesa"]
    if filtro == "categoria" and categoria:
        return [t for t in transacoes if t["categoria"] == categoria]
    return list(transacoes)

def totais(lista):
    r = sum(t["valor"] for t in lista if t["tipo"] == "receita")
    d = sum(t["valor"] for t in lista if t["tipo"] == "despesa")
    return r, d
