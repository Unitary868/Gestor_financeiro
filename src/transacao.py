
from utils import gerar_id_transacao

transacoes = {}
_id_global = 0

CATEGORIAS = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Salário", "Freelance", "Outros",
)


# CREATE
def adicionar_transacao(tipo, descricao, valor, categoria):
    # Validações AQUI (padrão prof)
    if tipo not in ["receita", "despesa"]:
        return 400, "Tipo inválido. Use 'receita' ou 'despesa'"
    if len(descricao.strip()) < 2:
        return 400, "Descrição deve ter pelo menos 2 caracteres"
    if valor <= 0:
        return 400, "Valor deve ser positivo"
    if categoria not in CATEGORIAS:
        return 400, f"Categoria inválida. Use: {', '.join(CATEGORIAS)}"

    global _id_global
    _id_global += 1
    id_transacao = _id_global

    transacao = {
        "id": id_transacao,
        "tipo": tipo,
        "descricao": descricao.strip(),
        "valor": valor,
        "categoria": categoria
    }

    transacoes[id_transacao] = transacao
    return 201, transacao


# READ (individual)
def encontrar_transacao(id_transacao):
    if id_transacao not in transacoes:
        return 404, f"Transação #{id_transacao} não encontrada."
    return 200, transacoes[id_transacao]


# READ (lista)
def listar_transacoes(filtro="todas", categoria=None):
    if not transacoes:
        return 404, "Não existem transações registadas."

    resultado = {}
    for id_t, t in transacoes.items():
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


# UPDATE
def editar_transacao(id_transacao, descricao=None, valor=None, categoria=None):
    if id_transacao not in transacoes:
        return 404, f"Transação #{id_transacao} não encontrada."

    t = transacoes[id_transacao]

    if descricao and len(descricao.strip()) < 2:
        return 400, "Descrição deve ter pelo menos 2 caracteres"
    if valor and valor <= 0:
        return 400, "Valor deve ser positivo"
    if categoria and categoria not in CATEGORIAS:
        return 400, f"Categoria inválida. Use: {', '.join(CATEGORIAS)}"

    if descricao:
        transacoes[id_transacao]["descricao"] = descricao.strip()
    if valor:
        transacoes[id_transacao]["valor"] = valor
    if categoria:
        transacoes[id_transacao]["categoria"] = categoria

    return 200, transacoes[id_transacao]


# DELETE
def apagar_transacao(id_transacao):
    if id_transacao not in transacoes:
        return 404, f"Transação #{id_transacao} não encontrada."
    del transacoes[id_transacao]
    return 200, f"Transação #{id_transacao} removida com sucesso."


# HELPERS (para main)
def calcular_saldo():
    if not transacoes:
        return 200, 0.0

    total = 0.0
    for t in transacoes.values():
        total += t["valor"] if t["tipo"] == "receita" else -t["valor"]
    return 200, total


def totais(lista_transacoes):
    receitas = sum(t["valor"] for t in lista_transacoes if t["tipo"] == "receita")
    despesas = sum(t["valor"] for t in lista_transacoes if t["tipo"] == "despesa")
    return 200, receitas, despesas