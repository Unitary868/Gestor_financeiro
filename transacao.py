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
    try:
        global _id_t
        _id_t += 1
        transacoes.append({
            "id": _id_t, "tipo": tipo,
            "descricao": descricao, "valor": valor, "categoria": categoria
        })
        return (201, f"Transação #{_id_t} criada com sucesso.")
    except Exception as e:
        return (500, str(e))

def encontrar_transacao(id_t):
    try:
        for i, t in enumerate(transacoes):
            if t["id"] == id_t:
                return (200, i, t)
        return (404, f"Transação #{id_t} não encontrada.")
    except Exception as e:
        return (500, str(e))

def editar_transacao(id_t, desc=None, valor=None, cat=None):
    try:
        rc = encontrar_transacao(id_t)
        if rc[0] == 404:
            return (404, f"Transação #{id_t} não encontrada.")
        idx = rc[1]
        if desc:
            transacoes[idx]["descricao"] = desc
        if valor:
            transacoes[idx]["valor"]     = valor
        if cat:
            transacoes[idx]["categoria"] = cat
        return (200, f"Transação #{id_t} atualizada com sucesso.")
    except Exception as e:
        return (500, str(e))

def apagar_transacao(id_t):
    try:
        rc = encontrar_transacao(id_t)
        if rc[0] == 404:
            return (404, f"Transação #{id_t} não encontrada.")
        transacoes.pop(rc[1])
        return (200, f"Transação #{id_t} apagada com sucesso.")
    except Exception as e:
        return (500, str(e))

def listar_transacoes(filtro="todas", categoria=None):
    try:
        if filtro == "receitas":
            lst = [t for t in transacoes if t["tipo"] == "receita"]
        elif filtro == "despesas":
            lst = [t for t in transacoes if t["tipo"] == "despesa"]
        elif filtro == "categoria" and categoria:
            lst = [t for t in transacoes if t["categoria"] == categoria]
        else:
            lst = list(transacoes)
        return (200, lst)
    except Exception as e:
        return (500, str(e))

def totais(lista):
    try:
        r = sum(t["valor"] for t in lista if t["tipo"] == "receita")
        d = sum(t["valor"] for t in lista if t["tipo"] == "despesa")
        return (200, r, d)
    except Exception as e:
        return (500, str(e))

def calcular_saldo():
    try:
        total = 0.0
        for t in transacoes:
            total += t["valor"] if t["tipo"] == "receita" else -t["valor"]
        return (200, total)
    except Exception as e:
        return (500, str(e))

# ── Helper UI ─────────────────────────────────────────────────

def escolher_cat():
    for i, c in enumerate(CATEGORIAS, 1):
        print(f"    {i:2}. {c}")
    return CATEGORIAS[int(pedir_num(f"  Categoria (1-{len(CATEGORIAS)}): ", 1, len(CATEGORIAS), False)) - 1]
