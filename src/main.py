# ==============================
# main.py
# menu terminal para testar CRUD
# ==============================

from conta import (criar_conta, conta_existe, verificar_login,
                   get_nome, get_id, get_dados, atualizar_pin, eliminar_conta)
from transacao import (transacoes, adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes,
                       totais, calcular_saldo, CATEGORIAS)
from orcamento import (criar_orcamento, listar_orcamentos, consultar_orcamento,
                       atualizar_orcamento, remover_orcamento, registar_gasto, CATEGORIAS_ORC)
from pagamento import (criar_pagamento, listar_pagamentos, consultar_pagamento,
                       atualizar_pagamento, marcar_pago, remover_pagamento,
                       totais_pagamentos, ESTADOS_PAG, METODOS_PAG)


# ── Helpers com códigos HTTP ───────────────────────────────────
def listar_opcoes(lista):
    for i, item in enumerate(lista, 1):
        print(f"{i} - {item}")
    while True:
        try:
            idx = int(input(f"Opção (1-{len(lista)}): ")) - 1
            if 0 <= idx < len(lista):
                return lista[idx]
            print("400: Opção inválida.")
        except ValueError:
            print("400: Deve ser um número.")


def pedir_float(msg, opcional=False):
    while True:
        raw = input(msg).strip().replace(",", ".")
        if opcional and raw == "":
            return 0.0
        try:
            v = float(raw)
            if v < 0:
                print("400: Valor inválido. Deve ser positivo (ex: 12.50, 100).")
                continue
            return v
        except ValueError:
            print("400: Formato inválido. Use: 12.50, 100, 0.01 (ponto decimal).")


def pedir_nif():
    while True:
        nif = input("NIF (9 dígitos): ").strip()
        if nif.isdigit() and len(nif) == 9:
            return nif
        print("400: NIF inválido. Deve ter exatamente 9 dígitos (ex: 123456789).")


def pedir_pin():
    while True:
        pin = input("PIN (4 dígitos): ").strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("400: PIN inválido. Deve ter exatamente 4 dígitos (ex: 1234).")


def pedir_id():
    while True:
        try:
            id_str = input("ID: ").strip()
            return int(id_str)
        except ValueError:
            print("400: ID inválido. Deve ser um número.")


# ── Menus (estrutura do prof) ─────────────────────────────────
def menu_auth():
    print("\n===== AUTENTICAÇÃO =====")
    print("1 - Criar conta")
    print("2 - Entrar")
    print("0 - Sair")


def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1 - Nova transação")
    print("2 - Extrato")
    print("3 - Editar transação")
    print("4 - Apagar transação")
    print("5 - Orçamentos")
    print("6 - Pagamentos")
    print("7 - Conta")
    print("0 - Sair")


def menu_orcamento():
    print("\n===== ORÇAMENTOS =====")
    print("1 - Criar  2 - Listar  3 - Consultar  4 - Atualizar  5 - Remover  0 - Voltar")


def menu_pagamento():
    print("\n===== PAGAMENTOS =====")
    print("1 - Criar  2 - Listar  3 - Consultar  4 - Atualizar  5 - Marcar pago  6 - Remover  0 - Voltar")


def menu_conta():
    print("\n===== CONTA =====")
    print("1 - Ver dados  2 - Atualizar PIN  3 - Eliminar conta  0 - Voltar")


# ── Autenticação ──────────────────────────────────────────────
def auth():
    while True:
        menu_auth()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome completo: ").strip()
            if not nome:
                print("400: Nome obrigatório.")
                continue
            nif = pedir_nif()
            pin = pedir_pin()
            si = pedir_float("Saldo inicial (€, enter para 0): ", opcional=True)

            code, obj = criar_conta(nome, nif, pin, si)
            if code == 201:
                print("Conta criada com sucesso: " + str(obj))
                if si > 0:
                    adicionar_transacao("receita", "Saldo inicial", si, "Outros")
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "2":
            uid = pedir_id()
            pin = pedir_pin()
            code, obj = verificar_login(uid, pin)
            if code == 200:
                print("Login bem-sucedido: " + str(obj))
                return True
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "0":
            print("A sair...")
            return False
        else:
            print("Opção inválida.")


# ── Programa principal (EXATA estrutura do prof) ───────────────
def main():
    if not auth():
        return

    while True:
        code_n, nome = get_nome()
        code_id, uid = get_id()
        code_s, saldo = calcular_saldo()
        print(f"\n{nome if code_n == 200 else '—'} | ID: {uid if code_id == 200 else '—'} | Saldo: {saldo:.2f}€")

        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tipo_num = input("Tipo (1-Receita / 2-Despesa): ")
            tipo = "receita" if tipo_num == "1" else "despesa"
            desc = input("Descrição: ").strip()
            if not desc:
                print("400: Descrição obrigatória.")
                continue
            valor = pedir_float("Valor (€): ")
            cat = listar_opcoes(CATEGORIAS)

            code, obj = adicionar_transacao(tipo, desc, valor, cat)
            if code == 201:
                print("Transação criada com sucesso: " + str(obj))
                if tipo == "despesa" and cat in CATEGORIAS_ORC:
                    code_o, msg_o = registar_gasto(cat, valor)
                    print(str(code_o) + ": " + msg_o)
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "2":
            print("\n1 - Todas  2 - Receitas  3 - Despesas  4 - Por categoria")
            f = input("Filtro: ")
            filtro = {"1": "todas", "2": "receitas", "3": "despesas", "4": "categoria"}.get(f, "todas")
            cat = listar_opcoes(CATEGORIAS) if f == "4" else None

            code, obj = listar_transacoes(filtro, cat)
            if code == 200:
                print("Extrato:")
                for t in obj:
                    sg = "+" if t["tipo"] == "receita" else "-"
                    print(f"  #{t['id']} | {t['tipo']} | {t['descricao']} | {sg}{t['valor']:.2f}€ | {t['categoria']}")
                code_t, rec, desp = totais(obj)
                if code_t == 200:
                    print(f"  Receitas: +{rec:.2f}€  |  Despesas: -{desp:.2f}€")
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "3":
            id_t = pedir_id()
            code, msg, t = encontrar_transacao(id_t)
            if code == 200:
                print(f"Transação #{t['id']}: {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€")
                nova_desc = input(f"Nova descrição (enter): ").strip() or None
                novo_val = pedir_float(f"Novo valor [{t['valor']:.2f}] (enter): ", opcional=True)
                nova_cat = listar_opcoes(CATEGORIAS) if input("Alterar categoria? (s/n): ").lower() == "s" else None

                code, obj = editar_transacao(id_t, nova_desc, novo_val, nova_cat)
                if code == 200:
                    print("Transação actualizada com sucesso: " + str(obj))
                else:
                    print(str(code) + ": " + str(obj))
            else:
                print(str(code) + ": " + msg)

        elif opcao == "4":
            id_t = pedir_id()
            code, msg, t = encontrar_transacao(id_t)
            if code == 200:
                print(f"Transação #{t['id']}: {t['descricao']}")
                if input("Confirmar apagar? (s/N): ").lower() == "s":
                    code, obj = apagar_transacao(id_t)
                    if code == 200:
                        print("Transação removida com sucesso: " + str(obj))
                    else:
                        print(str(code) + ": " + str(obj))
                else:
                    print("Cancelado.")
            else:
                print(str(code) + ": " + msg)

        elif opcao == "5":
            submenu_orcamento()

        elif opcao == "6":
            submenu_pagamento()

        elif opcao == "7":
            submenu_conta()

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida.")


# ── Submenus (chamados no main) ───────────────────────────────
def submenu_orcamento():
    while True:
        menu_orcamento()
        op = input("Escolha uma opção: ")
        if op == "1":
            cat = listar_opcoes(CATEGORIAS_ORC)
            limite = pedir_float("Limite (€): ")
            code, obj = criar_orcamento(cat, limite)
            if code == 201:
                print("Orçamento criado com sucesso: " + str(obj))
            else:
                print(str(code) + ": " + str(obj))
        elif op == "2":
            code, obj = listar_orcamentos()
            if code == 200:
                print("Lista de orçamentos:")
                for id_o, d in obj.items():
                    print(f"  ID: {id_o} | {d['categoria']} | Limite: {d['limite']:.2f}€ | Gasto: {d['gasto']:.2f}€")
            else:
                print(str(code) + ": " + str(obj))
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def submenu_pagamento():
    while True:
        menu_pagamento()
        op = input("Escolha uma opção: ")
        if op == "1":
            desc = input("Descrição: ").strip()
            if not desc:
                print("400: Descrição obrigatória.")
                continue
            valor = pedir_float("Valor (€): ")
            metodo = listar_opcoes(METODOS_PAG)
            data = input("Data de vencimento (YYYY-MM-DD): ")
            code, obj = criar_pagamento(desc, valor, metodo, data)
            if code == 201:
                print("Pagamento criado com sucesso: " + str(obj))
            else:
                print(str(code) + ": " + str(obj))
        elif op == "0":
            return
        else:
            print("Opção inválida.")


def submenu_conta():
    while True:
        menu_conta()
        op = input("Escolha uma opção: ")
        if op == "1":
            code, obj = get_dados()
            if code == 200:
                print("Dados da conta: " + str(obj))
            else:
                print(str(code) + ": " + str(obj))
        elif op == "0":
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()