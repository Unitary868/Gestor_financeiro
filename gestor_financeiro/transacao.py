# transacao.py – Entidade Transação

from utils import pedir_num, sep, cab, pausar

# ── Dados globais ─────────────────────────────────────────────

transacoes = []
_id_t      = 0

CATEGORIAS = (
    "Alimentação", "Transporte", "Lazer",    "Saúde",
    "Educação",    "Habitação",  "Vestuário", "Tecnologia",
    "Poupança",    "Salário",    "Freelance", "Outros",
)

# ── CRUD ──────────────────────────────────────────────────────

def adicionar_transacao(tipo, descricao, valor, categoria):
    global _id_t
    _id_t += 1
    transacoes.append({
        "id": _id_t, "tipo": tipo,
        "descricao": descricao, "valor": valor, "categoria": categoria
    })
    return _id_t

def encontrar_transacao(id_t):
    for i, t in enumerate(transacoes):
        if t["id"] == id_t:
            return i, t
    return -1, None

def editar_transacao(id_t, desc=None, valor=None, cat=None):
    idx, _ = encontrar_transacao(id_t)
    if idx == -1:
        return False
    if desc:  transacoes[idx]["descricao"] = desc
    if valor: transacoes[idx]["valor"]     = valor
    if cat:   transacoes[idx]["categoria"] = cat
    return True

def apagar_transacao(id_t):
    idx, _ = encontrar_transacao(id_t)
    if idx == -1:
        return False
    transacoes.pop(idx)
    return True

def listar_transacoes(filtro="todas", categoria=None):
    if filtro == "receitas":
        return [t for t in transacoes if t["tipo"] == "receita"]
    if filtro == "despesas":
        return [t for t in transacoes if t["tipo"] == "despesa"]
    if filtro == "categoria" and categoria:
        return [t for t in transacoes if t["categoria"] == categoria]
    return list(transacoes)

def totais(lista):
    r = sum(t["valor"] for t in lista if t["tipo"] == "receita")
    d = sum(t["valor"] for t in lista if t["tipo"] == "despesa")
    return r, d

def calcular_saldo():
    total = 0.0
    for t in transacoes:
        total += t["valor"] if t["tipo"] == "receita" else -t["valor"]
    return total

# ── Helper UI ─────────────────────────────────────────────────

def escolher_cat():
    for i, c in enumerate(CATEGORIAS, 1):
        print(f"    {i:2}. {c}")
    return CATEGORIAS[int(pedir_num(f"  Categoria (1-{len(CATEGORIAS)}): ", 1, len(CATEGORIAS), False)) - 1]
