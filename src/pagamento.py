
from utils import gerar_id_pagamento

pagamentos = {}

# Atributos da entidade Pagamento:
#   id           → identificador único
#   descricao    → descrição do pagamento
#   valor        → montante pago
#   data         → data do pagamento (YYYY-MM-DD)
#   metodo       → forma de pagamento
#   id_transacao → transação associada (opcional)

METODOS_PAG = ("MB Way", "Transferência", "Multibanco", "Dinheiro", "Cartão")


# ── Helpers internos ──────────────────────────────────────────

def _validar_valor(valor):
    try:
        return float(valor) > 0
    except (TypeError, ValueError):
        return False

def _validar_metodo(metodo):
    return metodo in METODOS_PAG

def _validar_data(data_texto):
    from datetime import datetime
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ── CREATE ────────────────────────────────────────────────────

def criar_pagamento(descricao, valor, data, metodo, id_transacao=None):
    if not descricao or not descricao.strip():
        return 400, "Descrição obrigatória."
    if not _validar_valor(valor):
        return 400, "Valor inválido. Deve ser um número positivo."
    if not _validar_data(data):
        return 400, "Data inválida. Utilize o formato YYYY-MM-DD."
    if not _validar_metodo(metodo):
        return 400, f"Método inválido. Opções: {', '.join(METODOS_PAG)}."

    id_pagamento = gerar_id_pagamento()

    pagamento = {
        "id":           id_pagamento,
        "descricao":    descricao.strip(),
        "valor":        float(valor),
        "data":         data,
        "metodo":       metodo,
        "id_transacao": id_transacao,   # pode ser None
    }

    pagamentos[id_pagamento] = pagamento
    return 201, pagamento


# ── READ (listar todos) ───────────────────────────────────────

def listar_pagamentos(metodo=None):
    if not pagamentos:
        return 404, "Não existem pagamentos registados."

    if metodo is not None:
        if not _validar_metodo(metodo):
            return 400, f"Método inválido. Opções: {', '.join(METODOS_PAG)}."
        filtrado = {k: v for k, v in pagamentos.items() if v["metodo"] == metodo}
        if not filtrado:
            return 404, f"Sem pagamentos com método '{metodo}'."
        return 200, filtrado

    return 200, pagamentos


# ── READ (consultar individual) ───────────────────────────────

def consultar_pagamento(id_pagamento):
    if id_pagamento not in pagamentos:
        return 404, "Pagamento não encontrado."
    return 200, pagamentos[id_pagamento]


# ── UPDATE ────────────────────────────────────────────────────

def atualizar_pagamento(id_pagamento, descricao=None, valor=None, data=None, metodo=None, id_transacao=None):
    if id_pagamento not in pagamentos:
        return 404, "Pagamento não encontrado."

    if descricao is not None:
        if not descricao.strip():
            return 400, "Descrição não pode ser vazia."
        pagamentos[id_pagamento]["descricao"] = descricao.strip()

    if valor is not None:
        if not _validar_valor(valor):
            return 400, "Valor inválido. Deve ser um número positivo."
        pagamentos[id_pagamento]["valor"] = float(valor)

    if data is not None:
        if not _validar_data(data):
            return 400, "Data inválida. Utilize o formato YYYY-MM-DD."
        pagamentos[id_pagamento]["data"] = data

    if metodo is not None:
        if not _validar_metodo(metodo):
            return 400, f"Método inválido. Opções: {', '.join(METODOS_PAG)}."
        pagamentos[id_pagamento]["metodo"] = metodo

    if id_transacao is not None:
        pagamentos[id_pagamento]["id_transacao"] = id_transacao

    return 200, pagamentos[id_pagamento]


# ── DELETE ────────────────────────────────────────────────────

def remover_pagamento(id_pagamento):
    if id_pagamento not in pagamentos:
        return 404, "Pagamento não encontrado."
    del pagamentos[id_pagamento]
    return 200, id_pagamento


# ── HELPERS para o main ───────────────────────────────────────

def total_pagamentos():
    """Devolve o total gasto em pagamentos."""
    total = sum(v["valor"] for v in pagamentos.values())
    return 200, round(total, 2)

def pagamentos_por_metodo():
    """Agrupa e soma os pagamentos por método."""
    resumo = {}
    for p in pagamentos.values():
        resumo[p["metodo"]] = resumo.get(p["metodo"], 0.0) + p["valor"]
    return 200, {k: round(v, 2) for k, v in resumo.items()}
