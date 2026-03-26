# operacoes.py – Metas, Empregos, Saldo e Resumo

from entidades import transacoes, adicionar_transacao

# ── Dados globais ─────────────────────────────────────────────

metas  = []   # lista de dicionários {id, nome, objetivo, atual}
_id_m  = 0    # contador de IDs de metas

EMPREGOS = [
    ("Programador",      25.0, 8), ("Designer Gráfico", 20.0, 8),
    ("Motorista",        12.0, 8), ("Professor",        18.0, 6),
    ("Médico",           40.0, 6), ("Engenheiro",       30.0, 8),
    ("Freelancer Web",   22.0, 4), ("Entregador",        9.0, 6),
    ("Rececionista",     10.0, 8), ("Consultor",        35.0, 4),
]

# ── Saldo ─────────────────────────────────────────────────────

def calcular_saldo():
    total = 0.0
    for t in transacoes:
        total += t["valor"] if t["tipo"] == "receita" else -t["valor"]
    return total

# ── Metas – CRUD ──────────────────────────────────────────────

def adicionar_meta(nome, objetivo):
    global _id_m
    _id_m += 1
    metas.append({"id": _id_m, "nome": nome, "objetivo": objetivo, "atual": 0.0})
    return _id_m

def encontrar_meta(id_m):
    for i, m in enumerate(metas):
        if m["id"] == id_m: return i, m
    return -1, None

def atribuir_valor_meta(id_m, valor):
    idx, m = encontrar_meta(id_m)
    if idx == -1: return False
    metas[idx]["atual"] += valor
    adicionar_transacao("despesa", f"Poupança: {m['nome']}", valor, "Poupança")
    return True

def apagar_meta(id_m):
    idx, _ = encontrar_meta(id_m)
    if idx == -1: return False
    metas.pop(idx); return True

def percentagem_meta(m):
    return 0.0 if m["objetivo"] == 0 else m["atual"] / m["objetivo"] * 100

# ── Empregos ──────────────────────────────────────────────────

def registar_trabalho(indice):
    nome, eur_h, h = EMPREGOS[indice]
    ganho = eur_h * h
    adicionar_transacao("receita", f"Trabalho: {nome}", ganho, "Salário")
    return ganho

# ── Resumo por categoria ──────────────────────────────────────

def gastos_por_categoria():
    gc = {}
    for t in transacoes:
        if t["tipo"] == "despesa":
            gc[t["categoria"]] = gc.get(t["categoria"], 0.0) + t["valor"]
    return dict(sorted(gc.items(), key=lambda x: x[1], reverse=True))
