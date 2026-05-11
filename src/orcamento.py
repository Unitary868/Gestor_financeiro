
from utils import gerar_id_orcamento

orcamentos = {}

# Atributos da entidade Orçamento:
#   id          → identificador único
#   categoria   → categoria associada ao orçamento
#   limite      → valor máximo definido
#   periodo     → período de validade (ex: "mensal", "semanal", "anual")
#   gasto_atual → valor já utilizado

CATEGORIAS_ORC = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Outros",
)

PERIODOS = ("diário", "semanal", "mensal", "anual")


# ── Helpers internos ──────────────────────────────────────────

def _validar_valor(valor):
    try:
        return float(valor) > 0
    except (TypeError, ValueError):
        return False

def _validar_categoria(categoria):
    return categoria in CATEGORIAS_ORC

def _validar_periodo(periodo):
    return periodo in PERIODOS


# ── CREATE ────────────────────────────────────────────────────

def criar_orcamento(categoria, limite, periodo):
    if not _validar_categoria(categoria):
        return 400, f"Categoria inválida. Opções: {', '.join(CATEGORIAS_ORC)}."
    if not _validar_valor(limite):
        return 400, "Limite inválido. Deve ser um número positivo."
    if not _validar_periodo(periodo):
        return 400, f"Período inválido. Opções: {', '.join(PERIODOS)}."

    # Não permitir duplicado de categoria + período
    for oid, o in orcamentos.items():
        if o["categoria"] == categoria and o["periodo"] == periodo:
            return 409, f"Já existe um orçamento para '{categoria}' ({periodo}) com ID {oid}."

    id_orcamento = gerar_id_orcamento()

    orcamento = {
        "id":          id_orcamento,
        "categoria":   categoria,
        "limite":      float(limite),
        "periodo":     periodo,
        "gasto_atual": 0.0,
    }

    orcamentos[id_orcamento] = orcamento
    return 201, orcamento


# ── READ (listar todos) ───────────────────────────────────────

def listar_orcamentos():
    if not orcamentos:
        return 404, "Não existem orçamentos registados."
    return 200, orcamentos


# ── READ (consultar individual) ───────────────────────────────

def consultar_orcamento(id_orcamento):
    if id_orcamento not in orcamentos:
        return 404, "Orçamento não encontrado."
    return 200, orcamentos[id_orcamento]


# ── UPDATE ────────────────────────────────────────────────────

def atualizar_orcamento(id_orcamento, limite=None, categoria=None, periodo=None):
    if id_orcamento not in orcamentos:
        return 404, "Orçamento não encontrado."

    if limite is not None:
        if not _validar_valor(limite):
            return 400, "Limite inválido. Deve ser um número positivo."
        orcamentos[id_orcamento]["limite"] = float(limite)

    if categoria is not None:
        if not _validar_categoria(categoria):
            return 400, f"Categoria inválida. Opções: {', '.join(CATEGORIAS_ORC)}."
        for oid, o in orcamentos.items():
            if o["categoria"] == categoria and o["periodo"] == orcamentos[id_orcamento]["periodo"] and oid != id_orcamento:
                return 409, "Já existe um orçamento para esta categoria e período."
        orcamentos[id_orcamento]["categoria"] = categoria

    if periodo is not None:
        if not _validar_periodo(periodo):
            return 400, f"Período inválido. Opções: {', '.join(PERIODOS)}."
        orcamentos[id_orcamento]["periodo"] = periodo

    return 200, orcamentos[id_orcamento]


# ── DELETE ────────────────────────────────────────────────────

def remover_orcamento(id_orcamento):
    if id_orcamento not in orcamentos:
        return 404, "Orçamento não encontrado."
    del orcamentos[id_orcamento]
    return 200, id_orcamento


# ── Registar gasto (chamado ao adicionar uma despesa) ────────

def registar_gasto(id_orcamento, valor):
    if id_orcamento not in orcamentos:
        return 404, "Orçamento não encontrado."
    if not _validar_valor(valor):
        return 400, "Valor inválido."

    orcamentos[id_orcamento]["gasto_atual"] += float(valor)
    restante = orcamentos[id_orcamento]["limite"] - orcamentos[id_orcamento]["gasto_atual"]
    categoria = orcamentos[id_orcamento]["categoria"]

    if restante < 0:
        return 200, f"AVISO: Orçamento '{categoria}' excedido em {abs(round(restante, 2))}€!"
    return 200, f"Gasto registado. Restam {round(restante, 2)}€ no orçamento '{categoria}'."
