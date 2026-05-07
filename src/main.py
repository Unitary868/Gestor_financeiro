# ==============================
# main.py
# ==============================

from conta import (criar_conta, conta_existe, verificar_login,
                   get_nome, get_id, get_dados, atualizar_pin, eliminar_conta)
from transacao import (adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes,
                       totais, calcular_saldo, CATEGORIAS)
from orcamento import (criar_orcamento, listar_orcamentos, consultar_orcamento,
                       atualizar_orcamento, remover_orcamento, registar_gasto,
                       CATEGORIAS_ORC, PERIODOS)
from pagamento import (criar_pagamento, listar_pagamentos, consultar_pagamento,
                       atualizar_pagamento, remover_pagamento, METODOS_PAG)


_id_conta_logada = None


# ── Helpers ───────────────────────────────────────────────────

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
            return None
        try:
            v = float(raw)
            if v <= 0:
                print("400: Valor deve ser positivo.")
                continue
            return v
        except ValueError:
            print("400: Formato inválido. Use: 12.50 ou 100.")

def pedir_nif():
    while True:
        nif = input("NIF (9 dígitos): ").strip()
        if nif.isdigit() and len(nif) == 9:
            return nif
        print("400: NIF inválido.")

def pedir_pin(msg="PIN (4 dígitos): "):
    while True:
        pin = input(msg).strip()
        if pin.isdigit() and len(pin) == 4:
            return pin
        print("400: PIN inválido.")

def pedir_id(msg="ID: "):
    return input(msg).strip().upper()


# ── Menus ─────────────────────────────────────────────────────

def menu_auth():
    print("\n===== AUTENTICAÇÃO =====")
    print("1 - Criar conta\n2 - Entrar\n0 - Sair")

def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1 - Nova transação\n2 - Extrato\n3 - Editar transação")
    print("4 - Apagar transação\n5 - Orçamentos\n6 - Pagamentos\n7 - Conta\n0 - Sair")

def menu_orcamento():
    print("\n===== ORÇAMENTOS =====")
    print("1-Criar  2-Listar  3-Consultar  4-Atualizar  5-Remover  0-Voltar")

def menu_pagamento():
    print("\n===== PAGAMENTOS =====")
    print("1-Criar  2-Listar  3-Consultar  4-Atualizar  5-Remover  0-Voltar")

def menu_conta():
    print("\n===== CONTA =====")
    print("1-Ver dados  2-Atualizar PIN  3-Eliminar conta  0-Voltar")


# ── Auth ──────────────────────────────────────────────────────

def auth():
    global _id_conta_logada
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
            code, obj = criar_conta(nome, nif, pin)
            if code == 201:
                print(f"201: Conta criada! ID: {obj['id']}")
            else:
                print(f"{code}: {obj}")

        elif opcao == "2":
            uid = pedir_id("ID da conta: ")
            pin = pedir_pin()
            code, obj = verificar_login(uid, pin)
            if code == 200:
                _id_conta_logada = uid
                print(f"200: Bem-vindo, {obj['nome']}!")
                return True
            else:
                print(f"{code}: {obj}")

        elif opcao == "0":
            print("A sair...")
            return False
        else:
            print("Opção inválida.")


# ── Main ──────────────────────────────────────────────────────

def main():
    global _id_conta_logada
    if not auth():
        return

    while True:
        code_n, nome = get_nome(_id_conta_logada)
        code_s, saldo = calcular_saldo(_id_conta_logada)
        print(f"\n{nome if code_n == 200 else '—'} | ID: {_id_conta_logada} | Saldo: {saldo:.2f}€")

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
            cat = listar_opcoes(list(CATEGORIAS))
            id_orc = input("ID orçamento (enter para ignorar): ").strip().upper() or None

            code, obj = adicionar_transacao(tipo, desc, valor, cat, _id_conta_logada, id_orc)
            if code == 201:
                print(f"201: Transação criada! {obj}")
                if tipo == "despesa" and id_orc:
                    code_o, msg_o = registar_gasto(id_orc, valor)
                    print(f"{code_o}: {msg_o}")
            else:
                print(f"{code}: {obj}")

        elif opcao == "2":
            print("\n1-Todas  2-Receitas  3-Despesas  4-Por categoria")
            f = input("Filtro: ")
            filtro = {"1": "todas", "2": "receitas", "3": "despesas", "4": "categoria"}.get(f, "todas")
            cat = listar_opcoes(list(CATEGORIAS)) if f == "4" else None

            code, obj = listar_transacoes(_id_conta_logada, filtro, cat)
            if code == 200:
                print("Extrato:")
                for t in obj:
                    sg = "+" if t["tipo"] == "receita" else "-"
                    print(f"  {t['id']} | {t['tipo']:7} | {t['descricao']:20} | {sg}{t['valor']:.2f}€ | {t['categoria']}")
                code_t, rec, desp = totais(_id_conta_logada)
                if code_t == 200:
                    print(f"  Receitas: +{rec:.2f}€  |  Despesas: -{desp:.2f}€")
            else:
                print(f"{code}: {obj}")

        elif opcao == "3":
            id_t = pedir_id("ID da transação: ")
            code, obj = encontrar_transacao(id_t)
            if code != 200:
                print(f"{code}: {obj}")
                continue
            print(f"  {obj['id']} | {obj['tipo']} | {obj['descricao']} | {obj['valor']:.2f}€")
            nova_desc = input("Nova descrição (enter para manter): ").strip() or None
            novo_val  = pedir_float("Novo valor (enter para manter): ", opcional=True)
            nova_cat  = listar_opcoes(list(CATEGORIAS)) if input("Alterar categoria? (s/n): ").lower() == "s" else None
            code, obj = editar_transacao(id_t, nova_desc, novo_val, nova_cat)
            print(f"{code}: {obj}")

        elif opcao == "4":
            id_t = pedir_id("ID da transação: ")
            code, obj = encontrar_transacao(id_t)
            if code != 200:
                print(f"{code}: {obj}")
                continue
            print(f"  {obj['id']} | {obj['descricao']} | {obj['valor']:.2f}€")
            if input("Confirmar apagar? (s/N): ").lower() == "s":
                code, msg = apagar_transacao(id_t)
                print(f"{code}: {msg}")
            else:
                print("Cancelado.")

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


# ── Submenus ──────────────────────────────────────────────────

def submenu_orcamento():
    while True:
        menu_orcamento()
        op = input("Escolha uma opção: ")

        if op == "1":
            cat     = listar_opcoes(list(CATEGORIAS_ORC))
            limite  = pedir_float("Limite (€): ")
            periodo = listar_opcoes(list(PERIODOS))
            code, obj = criar_orcamento(cat, limite, periodo)
            print(f"{code}: {obj}")

        elif op == "2":
            code, obj = listar_orcamentos()
            if code == 200:
                for id_o, d in obj.items():
                    restante = d["limite"] - d["gasto_atual"]
                    print(f"  {id_o} | {d['categoria']} | {d['periodo']} | Limite: {d['limite']:.2f}€ | Gasto: {d['gasto_atual']:.2f}€ | Restante: {restante:.2f}€")
            else:
                print(f"{code}: {obj}")

        elif op == "3":
            id_o = pedir_id("ID do orçamento: ")
            code, obj = consultar_orcamento(id_o)
            print(f"{code}: {obj}")

        elif op == "4":
            id_o   = pedir_id("ID do orçamento: ")
            novo_l = pedir_float("Novo limite (enter para manter): ", opcional=True)
            nova_c = listar_opcoes(list(CATEGORIAS_ORC)) if input("Alterar categoria? (s/n): ").lower() == "s" else None
            novo_p = listar_opcoes(list(PERIODOS)) if input("Alterar período? (s/n): ").lower() == "s" else None
            code, obj = atualizar_orcamento(id_o, novo_l, nova_c, novo_p)
            print(f"{code}: {obj}")

        elif op == "5":
            id_o = pedir_id("ID do orçamento: ")
            if input("Confirmar? (s/N): ").lower() == "s":
                code, obj = remover_orcamento(id_o)
                print(f"{code}: {obj}")
            else:
                print("Cancelado.")

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
            valor  = pedir_float("Valor (€): ")
            data   = input("Data (YYYY-MM-DD): ").strip()
            metodo = listar_opcoes(list(METODOS_PAG))
            id_t   = input("ID transação associada (enter para ignorar): ").strip().upper() or None
            code, obj = criar_pagamento(desc, valor, data, metodo, id_t)
            print(f"{code}: {obj}")

        elif op == "2":
            code, obj = listar_pagamentos()
            if code == 200:
                for id_p, p in obj.items():
                    print(f"  {id_p} | {p['descricao']} | {p['valor']:.2f}€ | {p['data']} | {p['metodo']}")
            else:
                print(f"{code}: {obj}")

        elif op == "3":
            id_p = pedir_id("ID do pagamento: ")
            code, obj = consultar_pagamento(id_p)
            print(f"{code}: {obj}")

        elif op == "4":
            id_p    = pedir_id("ID do pagamento: ")
            nova_d  = input("Nova descrição (enter para manter): ").strip() or None
            novo_v  = pedir_float("Novo valor (enter para manter): ", opcional=True)
            nova_dt = input("Nova data (enter para manter): ").strip() or None
            novo_m  = listar_opcoes(list(METODOS_PAG)) if input("Alterar método? (s/n): ").lower() == "s" else None
            code, obj = atualizar_pagamento(id_p, nova_d, novo_v, nova_dt, novo_m)
            print(f"{code}: {obj}")

        elif op == "5":
            id_p = pedir_id("ID do pagamento: ")
            if input("Confirmar? (s/N): ").lower() == "s":
                code, obj = remover_pagamento(id_p)
                print(f"{code}: {obj}")
            else:
                print("Cancelado.")

        elif op == "0":
            return
        else:
            print("Opção inválida.")


def submenu_conta():
    global _id_conta_logada
    while True:
        menu_conta()
        op = input("Escolha uma opção: ")

        if op == "1":
            code, obj = get_dados(_id_conta_logada)
            if code == 200:
                print(f"  Nome: {obj['nome']} | NIF: {obj['nif']} | Token: {obj['token']}")
            else:
                print(f"{code}: {obj}")

        elif op == "2":
            pin_atual = pedir_pin("PIN atual: ")
            pin_novo  = pedir_pin("Novo PIN: ")
            code, obj = atualizar_pin(_id_conta_logada, pin_atual, pin_novo)
            print(f"{code}: {'PIN atualizado!' if code == 200 else obj}")

        elif op == "3":
            pin = pedir_pin("PIN para confirmar: ")
            if input("Tens a certeza? (s/N): ").lower() == "s":
                code, obj = eliminar_conta(_id_conta_logada, pin)
                if code == 200:
                    print("200: Conta eliminada. A sair...")
                    _id_conta_logada = None
                    return
                else:
                    print(f"{code}: {obj}")
            else:
                print("Cancelado.")

        elif op == "0":
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
