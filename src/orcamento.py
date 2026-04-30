from utils import pedir_num

# ── Dados globais ─────────────────────────────────────────────

orcamentos = {}
_id_o = 0

CATEGORIAS_ORC = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Outros",
)

# ── Helpers internos ──────────────────────────────────────────

def _gerar_id():
    global _id_o
    _id_o += 1
    return f"O{_id_o:03d}"

def _validar_valor(valor):
    try:
        v = float(valor)
        return v > 0
    except (TypeError, ValueError):
        return False

def _validar_categoria(categoria):
    return categoria in CATEGORIAS_ORC

# ── CREATE ────────────────────────────────────────────────────

def criar_orcamento(categoria, limite):
    try:
        if not _validar_categoria(categoria):
            return 400, "Categoria inválida."
        if not _validar_valor(limite):
            return 400, "Limite inválido. Deve ser um número positivo."
        for oid, o in orcamentos.items():
            if o["categoria"] == categoria:
                return 409, "Já existe um orçamento para esta categoria (ID: " + oid + ")."
        id_orcamento = _gerar_id()
        orcamento = {
            "categoria": categoria,
            "limite": float(limite),
            "gasto": 0.0,
        }
        orcamentos[id_orcamento] = orcamento
        return 201, orcamento
    except Exception as e:
        return 500, str(e)

# ── READ (listar todos) ───────────────────────────────────────

def listar_orcamentos():
    try:
        if not orcamentos:
            return 404, "Não existem orçamentos registados."
        return 200, orcamentos
    except Exception as e:
        return 500, str(e)

# ── READ (consultar individual) ───────────────────────────────

def consultar_orcamento(id_orcamento):
    try:
        if id_orcamento not in orcamentos:
            return 404, "Orçamento não encontrado."
        orcamento = orcamentos[id_orcamento]
        return 200, orcamento
    except Exception as e:
        return 500, str(e)

# ── UPDATE ────────────────────────────────────────────────────

def atualizar_orcamento(id_orcamento, limite=None, categoria=None):
    try:
        if id_orcamento not in orcamentos:
            return 404, "Orçamento não encontrado."
        if limite is not None:
            if not _validar_valor(limite):
                return 400, "Limite inválido. Deve ser um número positivo."
            orcamentos[id_orcamento]["limite"] = float(limite)
        if categoria is not None:
            if not _validar_categoria(categoria):
                return 400, "Categoria inválida."
            for oid, o in orcamentos.items():
                if o["categoria"] == categoria and oid != id_orcamento:
                    return 409, "Já existe um orçamento para esta categoria."
            orcamentos[id_orcamento]["categoria"] = categoria
        return 200, orcamentos[id_orcamento]
    except Exception as e:
        return 500, str(e)

# ── DELETE ────────────────────────────────────────────────────

def remover_orcamento(id_orcamento):
    try:
        if id_orcamento not in orcamentos:
            return 404, "Orçamento não encontrado."
        del orcamentos[id_orcamento]
        return 200, id_orcamento
    except Exception as e:
        return 500, str(e)

# ── Registar gasto (chamado quando adicionas uma despesa) ─────

def registar_gasto(categoria, valor):
    try:
        if not _validar_valor(valor):
            return 400, "Valor inválido."
        for oid, o in orcamentos.items():
            if o["categoria"] == categoria:
                orcamentos[oid]["gasto"] += float(valor)
                restante = o["limite"] - orcamentos[oid]["gasto"]
                if restante < 0:
                    return 200, "AVISO: Orçamento '" + categoria + "' excedido em " + str(abs(round(restante, 2))) + "€!"
                return 200, "Gasto registado. Restam " + str(round(restante, 2)) + "€ no orçamento '" + categoria + "'."
        return 200, "Sem orçamento definido para esta categoria."
    except Exception as e:
        return 500, str(e)