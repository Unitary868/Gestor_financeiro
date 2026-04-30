from utils import pedir_num

# ── Dados globais ─────────────────────────────────────────────

pagamentos = {}
_id_p = 0

ESTADOS_PAG = ("pendente", "pago", "cancelado")
METODOS_PAG = ("MB Way", "Transferência", "Multibanco", "Dinheiro", "Cartão")

# ── Helpers internos ──────────────────────────────────────────

def _gerar_id():
    global _id_p
    _id_p += 1
    return f"P{_id_p:03d}"

def _validar_valor(valor):
    try:
        v = float(valor)
        return v > 0
    except (TypeError, ValueError):
        return False

def _validar_estado(estado):
    return estado in ESTADOS_PAG

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

def criar_pagamento(descricao, valor, metodo, data_vencimento):
    try:
        if not descricao or not descricao.strip():
            return 400, "Descrição obrigatória."
        if not _validar_valor(valor):
            return 400, "Valor inválido. Deve ser um número positivo."
        if not _validar_metodo(metodo):
            return 400, "Método de pagamento inválido."
        if not _validar_data(data_vencimento):
            return 400, "Data inválida. Utilize o formato YYYY-MM-DD."
        id_pagamento = _gerar_id()
        pagamento = {
            "descricao": descricao.strip(),
            "valor": float(valor),
            "metodo": metodo,
            "data_vencimento": data_vencimento,
            "estado": "pendente",
        }
        pagamentos[id_pagamento] = pagamento
        return 201, pagamento
    except Exception as e:
        return 500, str(e)

# ── READ (listar todos) ───────────────────────────────────────

def listar_pagamentos(estado=None):
    try:
        if not pagamentos:
            return 404, "Não existem pagamentos registados."
        if estado:
            if not _validar_estado(estado):
                return 400, "Estado inválido."
            filtrado = {k: v for k, v in pagamentos.items() if v["estado"] == estado}
            if not filtrado:
                return 404, "Sem pagamentos com estado '" + estado + "'."
            return 200, filtrado
        return 200, pagamentos
    except Exception as e:
        return 500, str(e)

# ── READ (consultar individual) ───────────────────────────────

def consultar_pagamento(id_pagamento):
    try:
        if id_pagamento not in pagamentos:
            return 404, "Pagamento não encontrado."
        pagamento = pagamentos[id_pagamento]
        return 200, pagamento
    except Exception as e:
        return 500, str(e)

# ── UPDATE ────────────────────────────────────────────────────

def atualizar_pagamento(id_pagamento, descricao=None, valor=None, metodo=None, data_vencimento=None, estado=None):
    try:
        if id_pagamento not in pagamentos:
            return 404, "Pagamento não encontrado."
        if pagamentos[id_pagamento]["estado"] == "cancelado":
            return 409, "Não é possível editar um pagamento cancelado."
        if descricao is not None:
            if not descricao.strip():
                return 400, "Descrição não pode ser vazia."
            pagamentos[id_pagamento]["descricao"] = descricao.strip()
        if valor is not None:
            if not _validar_valor(valor):
                return 400, "Valor inválido. Deve ser um número positivo."
            pagamentos[id_pagamento]["valor"] = float(valor)
        if metodo is not None:
            if not _validar_metodo(metodo):
                return 400, "Método de pagamento inválido."
            pagamentos[id_pagamento]["metodo"] = metodo
        if data_vencimento is not None:
            if not _validar_data(data_vencimento):
                return 400, "Data inválida. Utilize o formato YYYY-MM-DD."
            pagamentos[id_pagamento]["data_vencimento"] = data_vencimento
        if estado is not None:
            if not _validar_estado(estado):
                return 400, "Estado inválido."
            pagamentos[id_pagamento]["estado"] = estado
        return 200, pagamentos[id_pagamento]
    except Exception as e:
        return 500, str(e)

# ── Marcar como pago (atalho) ─────────────────────────────────

def marcar_pago(id_pagamento):
    try:
        if id_pagamento not in pagamentos:
            return 404, "Pagamento não encontrado."
        if pagamentos[id_pagamento]["estado"] == "pago":
            return 409, "Pagamento já está marcado como pago."
        if pagamentos[id_pagamento]["estado"] == "cancelado":
            return 409, "Não é possível marcar como pago um pagamento cancelado."
        pagamentos[id_pagamento]["estado"] = "pago"
        return 200, pagamentos[id_pagamento]
    except Exception as e:
        return 500, str(e)

# ── DELETE ────────────────────────────────────────────────────

def remover_pagamento(id_pagamento):
    try:
        if id_pagamento not in pagamentos:
            return 404, "Pagamento não encontrado."
        del pagamentos[id_pagamento]
        return 200, id_pagamento
    except Exception as e:
        return 500, str(e)

# ── Totais ────────────────────────────────────────────────────

def totais_pagamentos():
    try:
        pendentes  = sum(v["valor"] for v in pagamentos.values() if v["estado"] == "pendente")
        pagos      = sum(v["valor"] for v in pagamentos.values() if v["estado"] == "pago")
        cancelados = sum(v["valor"] for v in pagamentos.values() if v["estado"] == "cancelado")
        return 200, pendentes, pagos, cancelados
    except Exception as e:
        return 500, str(e)