# ==============================
# transacao.py
# CRUD simples para entidade Transação
# SEM utilização de classes
# Armazenamento em dicionário
# Validações feitas aqui (não no main)
# ==============================

from utils import gerar_id_transacao

transacoes = {}

# Atributos da entidade Transação:
#   id           → identificador único
#   tipo         → "receita" ou "despesa"
#   descricao    → descrição do movimento
#   valor        → montante em euros
#   categoria    → tipo de transação
#   id_conta     → conta associada
#   id_orcamento → orçamento associado (opcional)

CATEGORIAS = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Salário", "Freelance", "Outros",
)


# ── Helpers internos ──────────────────────────────────────────

def _validar_valor(valor):
    try:
        return float(valor) > 0
    except (TypeError, ValueError):
        return False


# ── CREATE ────────────────────────────────────────────────────

def adicionar_transacao(tipo, descricao, valor, categoria, id_conta, id_orcamento=None):
    if tipo not in ("receita", "despesa"):
        return 400, "Tipo inválido. Use 'receita' ou 'despesa'."
    if len(descricao.strip()) < 2:
        return 400, "Descrição deve ter pelo menos 2 caracteres."
    if not _validar_valor(valor):
        return 400, "Valor deve ser um número positivo."
    if categoria not in CATEGORIAS:
        return 400, f"Categoria inválida. Opções: {', '.join(CATEGORIAS)}."
    if not id_conta:
        return 400, "id_conta é obrigatório."

    id_transacao = gerar_id_transacao()

    transacao = {
        "id":           id_transacao,
        "tipo":         tipo,
        "descricao":    descricao.strip(),
        "valor":        float(valor),
        "categoria":    categoria,
        "id_conta":     id_conta,
        "id_orcamento": id_orcamento,   # pode ser None
    }

    transacoes[id_transacao] = transacao
    return 201, transacao


# ── READ (individual) ─────────────────────────────────────────

def encontrar_transacao(id_transacao):
    if id_transacao not in transacoes:
        return 404, f"Transação {id_transacao} não encontrada."
    return 200, transacoes[id_transacao]


# ── READ (lista) ──────────────────────────────────────────────

def listar_transacoes(id_conta=None, filtro="todas", categoria=None):
    if not transacoes:
        return 404, "Não existem transações registadas."

    resultado = {}
    for id_t, t in transacoes.items():
        if id_conta and t["id_conta"] != id_conta:
            continue
        if filtro == "receitas" and t["tipo"] != "receita":
            continue
        if filtro == "despesas" and t["tipo"] != "despesa":
            continue
        if filtro == "categoria" and t["categoria"] != categoria:
            continue
        resultado[id_t] = t

    if not resultado:
        return 404, "Nenhuma transação encontrada com esse filtro."
    return 200, list(resultado.values())


# ── UPDATE ────────────────────────────────────────────────────

def editar_transacao(id_transacao, descricao=None, valor=None, categoria=None, id_orcamento=None):
    if id_transacao not in transacoes:
        return 404, f"Transação {id_transacao} não encontrada."

    if descricao is not None:
        if len(descricao.strip()) < 2:
            return 400, "Descrição deve ter pelo menos 2 caracteres."
        transacoes[id_transacao]["descricao"] = descricao.strip()

    if valor is not None:
        if not _validar_valor(valor):
            return 400, "Valor deve ser um número positivo."
        transacoes[id_transacao]["valor"] = float(valor)

    if categoria is not None:
        if categoria not in CATEGORIAS:
            return 400, f"Categoria inválida. Opções: {', '.join(CATEGORIAS)}."
        transacoes[id_transacao]["categoria"] = categoria

    if id_orcamento is not None:
        transacoes[id_transacao]["id_orcamento"] = id_orcamento

    return 200, transacoes[id_transacao]


# ── DELETE ────────────────────────────────────────────────────

def apagar_transacao(id_transacao):
    if id_transacao not in transacoes:
        return 404, f"Transação {id_transacao} não encontrada."
    del transacoes[id_transacao]
    return 200, f"Transação {id_transacao} removida com sucesso."


# ── HELPERS para o main ───────────────────────────────────────

def calcular_saldo(id_conta):
    """Calcula o saldo de uma conta somando receitas e subtraindo despesas."""
    total = 0.0
    for t in transacoes.values():
        if t["id_conta"] != id_conta:
            continue
        total += t["valor"] if t["tipo"] == "receita" else -t["valor"]
    return 200, total

def totais(id_conta=None):
    """Devolve (receitas_total, despesas_total) opcionalmente filtrado por conta."""
    lista = [
        t for t in transacoes.values()
        if id_conta is None or t["id_conta"] == id_conta
    ]
    receitas  = sum(t["valor"] for t in lista if t["tipo"] == "receita")
    despesas  = sum(t["valor"] for t in lista if t["tipo"] == "despesa")
    return 200, receitas, despesas