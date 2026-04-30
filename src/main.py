
from conta import (criar_conta, conta_existe, verificar_login,
                   get_nome, get_id, get_dados, atualizar_pin, eliminar_conta)
from transacao import (transacoes, adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes,
                       totais, calcular_saldo, CATEGORIAS)

# ── Menus ──────────────────────────────────────────────────────

def menu_auth():
    print("\n===== FINANÇAS PRO =====")
    print("1 - Criar conta")
    print("2 - Entrar")
    print("0 - Sair")

def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1 - Nova transação")
    print("2 - Ver extrato")
    print("3 - Editar transação")
    print("4 - Apagar transação")
    print("5 - Conta")
    print("0 - Sair")

def menu_conta():
    print("\n===== CONTA =====")
    print("1 - Ver dados")
    print("2 - Atualizar PIN")
    print("3 - Eliminar conta")
    print("0 - Voltar")

def menu_extrato():
    print("\n===== EXTRATO =====")
    print("1 - Todas")
    print("2 - Receitas")
    print("3 - Despesas")
    print("4 - Por categoria")

def menu_categorias():
    print("\n===== CATEGORIAS =====")
    for i, c in enumerate(CATEGORIAS, 1):
        print(f"{i} - {c}")

# ── Autenticação ───────────────────────────────────────────────

def auth():
    while True:
        menu_auth()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome completo: ")
            nif = input("NIF (9 dígitos): ")
            pin = input("PIN (4 dígitos): ")
            si = input("Saldo inicial (€): ")
            si = float(si) if si else 0.0
            code, obj = criar_conta(nome, nif, pin, si)
            if code == 201:
                print("Conta criada com sucesso. " + str(obj))
                if si > 0:
                    adicionar_transacao("receita", "Saldo inicial", si, "Outros")
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "2":
            code_ex, existe = conta_existe()
            if code_ex == 200 and not existe:
                print("404: Registe-se primeiro.")
                continue
            uid = input("ID: ")
            pin = input("PIN: ")
            code, obj = verificar_login(int(uid), pin)
            if code == 200:
                print("Login bem-sucedido. " + str(obj))
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "0":
            print("A sair...")
            return False

        else:
            print("Opção inválida.")

# ── Submenu Conta ──────────────────────────────────────────────

def submenu_conta():
    code_id, uid = get_id()
    while True:
        menu_conta()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            code, obj = get_dados()
            if code == 200:
                print("Dados da conta: " + str(obj))
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "2":
            pin_atual = input("PIN atual: ")
            pin_novo = input("PIN novo: ")
            code, obj = atualizar_pin(uid, pin_atual, pin_novo)
            if code == 200:
                print("PIN atualizado com sucesso. " + str(obj))
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "3":
            pin = input("PIN: ")
            confirmar = input("Tens a certeza? Todos os dados serão apagados (s/n): ")
            if confirmar.lower() == "s":
                code, obj = eliminar_conta(uid, pin)
                if code == 200:
                    print("Conta eliminada com sucesso. " + str(obj))
                    transacoes.clear()
                    return True
                else:
                    print(str(code) + ": " + str(obj))
            else:
                print("Cancelado.")

        elif opcao == "0":
            return False

        else:
            print("Opção inválida.")

# ── Programa principal ─────────────────────────────────────────

def main():
    if not auth():
        return

    while True:
        code_id, uid   = get_id()
        code_n,  nome  = get_nome()
        code_s,  saldo = calcular_saldo()
        print(f"\n{nome if code_n == 200 else '—'} | ID: {uid if code_id == 200 else '—'} | Saldo: {saldo:.2f}€ | Transações: {len(transacoes)}")

        menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            tipo = input("Tipo (1-Receita / 2-Despesa): ")
            tipo = "receita" if tipo == "1" else "despesa"
            desc = input("Descrição: ")
            valor = float(input("Valor (€): "))
            menu_categorias()
            cat_idx = int(input(f"Categoria (1-{len(CATEGORIAS)}): ")) - 1
            cat = CATEGORIAS[cat_idx]
            code, obj = adicionar_transacao(tipo, desc, valor, cat)
            if code == 201:
                print("Transação criada com sucesso. " + str(obj))
            else:
                print(str(code) + ": " + str(obj))

        elif opcao == "2":
            menu_extrato()
            f = input("Filtro: ")
            filtros = {"1": "todas", "2": "receitas", "3": "despesas", "4": "categoria"}
            filtro = filtros.get(f, "todas")
            cat = None
            if f == "4":
                menu_categorias()
                cat_idx = int(input(f"Categoria (1-{len(CATEGORIAS)}): ")) - 1
                cat = CATEGORIAS[cat_idx]
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
            id_t = int(input("ID da transação: "))
            code, *rest = encontrar_transacao(id_t)
            if code == 200:
                t = rest[1]
                print(f"Atual: {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€ | {t['categoria']}")
                nova_desc = input(f"Descrição [{t['descricao']}] (enter para manter): ") or None
                novo_val_str = input(f"Valor [{t['valor']:.2f}] (enter para manter): ")
                novo_val = float(novo_val_str) if novo_val_str else None
                nova_cat = None
                if input("Alterar categoria? (s/n): ").lower() == "s":
                    menu_categorias()
                    cat_idx = int(input(f"Categoria (1-{len(CATEGORIAS)}): ")) - 1
                    nova_cat = CATEGORIAS[cat_idx]
                code, obj = editar_transacao(id_t, nova_desc, novo_val, nova_cat)
                if code == 200:
                    print("Transação atualizada com sucesso. " + str(obj))
                else:
                    print(str(code) + ": " + str(obj))
            else:
                print(str(code) + ": " + str(rest[0]))

        elif opcao == "4":
            id_t = int(input("ID da transação: "))
            code, *rest = encontrar_transacao(id_t)
            if code == 200:
                t = rest[1]
                print(f"Transação: {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€")
                if input("Confirma? (s/n): ").lower() == "s":
                    code, obj = apagar_transacao(id_t)
                    if code == 200:
                        print("Transação apagada com sucesso. " + str(obj))
                    else:
                        print(str(code) + ": " + str(obj))
                else:
                    print("Cancelado.")
            else:
                print(str(code) + ": " + str(rest[0]))

        elif opcao == "5":
            if submenu_conta():
                break

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
