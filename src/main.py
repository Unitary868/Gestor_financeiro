# main.py – Interface, Login/Registo e ponto de entrada

import os, time
from transacao import (transacoes, adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes,
                       totais, calcular_saldo, escolher_cat)
from conta import (criar_conta, conta_existe, verificar_login,
                   get_nome, get_id, get_token)

# ── Funções UI ────────────────────────────────────────────────

def limpar():
    os.system("cls" if os.name == "nt" else "clear")
def sep():
    print("─" * 60)
def cab(t):
    print("\n" + "═"*60 + f"\n  {t}\n" + "═"*60)
def pausar():
    input("\n  Pressione Enter para continuar...")

def pedir_num(msg, mn=None, mx=None, dec=True):
    while True:
        try:
            # ── Input e conversão ─────────────────────────────
            entrada = input(msg).strip().replace(",", ".")
            v = float(entrada) if dec else int(entrada)

            # ── Validação de intervalo ───────────────────────
            if (mn is None or v >= mn) and (mx is None or v <= mx):
                return v

            # ── Erro: fora do intervalo ──────────────────────
            print(f"  400 - Bad Request: Valor fora do intervalo {mn} – {mx}.")

        except ValueError:
            # ── Erro: não é número ───────────────────────────
            print("  400 - Bad Request: Número inválido.")

def pedir_texto(msg):
    while True:
        t = input(msg).strip()
        if t:
            return t
        print("  400 - Bad Request: Campo obrigatório.")

def pedir_nif():
    while True:
        n = input("  NIF (9 dígitos): ").strip()
        if n.isdigit() and len(n) == 9: return n
        print("  400 - Bad Request: NIF inválido, deve ter 9 dígitos.")

def pedir_pin():
    while True:
        # ── Input ────────────────────────────────────────────
        p = input("  PIN (4 dígitos): ").strip()

        # ── Validação ────────────────────────────────────────
        if p.isdigit() and len(p) == 4:
            return p

        # ── Erro ─────────────────────────────────────────────
        print("  400 - Bad Request: PIN inválido, deve ter 4 dígitos.")

def pedir_password():
    while True:
        p = input("  Password (mín. 6 caracteres): ")
        if len(p) < 6:
            print("  400 - Bad Request: Password demasiado curta."); continue
        c = input("  Confirmar password: ")
        if p == c: return p
        print("  400 - Bad Request: Passwords não coincidem.")

# ── Autenticação ──────────────────────────────────────────────

def registar():
    cab("📋 CRIAR CONTA")
    nome = pedir_texto("  Nome completo: ")
    nif  = pedir_nif()
    pin  = pedir_pin()
    _    = pedir_password()
    si   = pedir_num("  Saldo inicial (€): ", mn=0.0)
    rc = criar_conta(nome, nif, pin)
    print(f"  {rc[0]} - {rc[1]}")
    if rc[0] == 201:
        if si > 0:
            adicionar_transacao("receita", "Saldo inicial", si, "Outros")
        sep()
        print(f"\n  👤 {nome}  💰 {si:.2f}€")
        sep()
    pausar()

def login():
    cab("🔐 LOGIN")
    try:
        uid = int(input("  ID: ").strip())
    except ValueError:
        print("  400 - Bad Request: ID inválido."); pausar(); return False
    pin = input("  PIN: ").strip()
    rc = verificar_login(uid, pin)
    print(f"  {rc[0]} - {rc[1]}")
    if rc[0] == 200:
        nome_rc = get_nome()
        nome = nome_rc[1] if nome_rc[0] == 200 else "—"
        print(f"\n  ✅ Bem-vindo, {nome}!")
        time.sleep(1)
        return True
    pausar()
    return False

def menu_auth():
    while True:
        limpar()
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║          💶  FinançasPro - Gestor Financeiro             ║")
        print("╚══════════════════════════════════════════════════════════╝\n")
        sep(); print("  1 - Criar conta   2 - Entrar   0 - Sair"); sep()
        o = input("\n  Opção: ").strip()
        if o == "1":
            registar();
            return True
        elif o == "2":
            rc = conta_existe()
            if rc[0] == 500:
                print(f"  {rc[0]} - {rc[1]}"); pausar()
            elif not rc[1]:
                print("  404 - Not Found: Registe-se primeiro.");
                pausar()
            elif login():
                return True
        elif o == "0":
            limpar();
            print("\n  👋 Até à próxima!\n"); return False
        else:
            print("  400 - Bad Request: Opção inválida."); time.sleep(1)

# ── Transações ────────────────────────────────────────────────

def nova_transacao():
    cab("NOVA TRANSAÇÃO")
    tipo = "receita" if int(pedir_num("  1-Receita  2-Despesa: ", 1, 2, False)) == 1 else "despesa"
    d    = pedir_texto("  Descrição: ")
    v    = pedir_num("  Valor (€): ", mn=0.01)
    c    = escolher_cat()
    rc   = adicionar_transacao(tipo, d, v, c)
    print(f"  {rc[0]} - {rc[1]}")
    pausar()

def ver_extrato():
    cab("EXTRATO")
    if not transacoes:
        print("  404 - Not Found: Sem transações.");
        pausar();
        return
    print("  1-Todas  2-Receitas  3-Despesas  4-Categoria")
    f   = int(pedir_num("  Filtro: ", 1, 4, False))
    rc  = listar_transacoes(
        ["todas", "receitas", "despesas", "categoria"][f - 1],
        escolher_cat() if f == 4 else None
    )
    if rc[0] != 200:
        print(f"  {rc[0]} - {rc[1]}"); pausar(); return
    lst = rc[1]
    if not lst:
        print("  404 - Not Found: Sem resultados."); pausar(); return
    sep()
    print(f"  {'ID':<4} {'TIPO':<8} {'DESCRIÇÃO':<22} {'VALOR':>10}  CATEGORIA")
    sep()
    for t in lst:
        sg = "+" if t["tipo"] == "receita" else "-"
        print(f"  #{t['id']:<3} {'⬆' if t['tipo'] == 'receita' else '⬇'} {t['tipo']:<7} "
              f"{t['descricao']:<22} {sg}{t['valor']:>8.2f}€  {t['categoria']}")
    rc_t = totais(lst)
    if rc_t[0] == 200:
        sep(); print(f"  Receitas: +{rc_t[1]:.2f}€  Despesas: -{rc_t[2]:.2f}€"); sep()
    pausar()

def editar():
    # ── Cabeçalho ────────────────────────────────────────────
    cab("EDITAR TRANSAÇÃO")

    # ── Verificar se existem transações ──────────────────────
    if not transacoes:
        print("  404 - Not Found: Sem transações.")
        pausar()
        return

    # ── Pedir ID ─────────────────────────────────────────────
    id_t = int(pedir_num("  ID: ", 1, dec=False))

    # ── Procurar transação ───────────────────────────────────
    rc = encontrar_transacao(id_t)
    if rc[0] != 200:
        print(f"  {rc[0]} - {rc[1]}")
        pausar()
        return

    # ── Dados atuais ─────────────────────────────────────────
    t = rc[2]
    print(f"\n  Atual → {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€ | {t['categoria']}")

    # ── Nova descrição (opcional) ────────────────────────────
    nova_desc = input(f"  Descrição [{t['descricao']}]: ").strip()

    # ── Novo valor (opcional) ────────────────────────────────
    novo_valor = None
    entrada_valor = input(f"  Valor [{t['valor']:.2f}]: ").strip().replace(",", ".")

    if entrada_valor:
        try:
            valor_float = float(entrada_valor)
            if valor_float > 0:
                novo_valor = valor_float
        except ValueError:
            print("  400 - Bad Request: Valor inválido.")

    # ── Nova categoria (opcional) ────────────────────────────
    alterar_cat = input("  Alterar categoria? (s/n): ").strip().lower()
    nova_cat = escolher_cat() if alterar_cat == "s" else None

    # ── Atualizar transação ──────────────────────────────────
    rc = editar_transacao(
        id_t,
        nova_desc or None,
        novo_valor,
        nova_cat
    )

    print(f"  {rc[0]} - {rc[1]}")

    # ── Pausa final ──────────────────────────────────────────
    pausar()

def apagar():
    # ── Cabeçalho ────────────────────────────────────────────
    cab("APAGAR TRANSAÇÃO")

    # ── Verificar se existem transações ──────────────────────
    if not transacoes:
        print("  404 - Not Found: Sem transações.")
        pausar()
        return

    # ── Pedir ID ─────────────────────────────────────────────
    id_t = int(pedir_num("  ID: ", 1, dec=False))

    # ── Procurar transação ───────────────────────────────────
    rc = encontrar_transacao(id_t)
    if rc[0] != 200:
        print(f"  {rc[0]} - {rc[1]}")
        pausar()
        return

    # ── Mostrar dados da transação ───────────────────────────
    t = rc[2]
    print(f"\n  {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€")

    # ── Confirmação ──────────────────────────────────────────
    confirmacao = input("  Confirma? (s/n): ").strip().lower()

    if confirmacao == "s":
        rc = apagar_transacao(id_t)
        print(f"  {rc[0]} - {rc[1]}")
    else:
        print("  ❌ Cancelado.")

    # ── Pausa final ──────────────────────────────────────────
    pausar()

# ── Menu Principal ────────────────────────────────────────────

def menu_principal():
    # ── Mapeamento de ações ──────────────────────────────────
    acoes = {
        "1":
        nova_transacao,
        "2":
        ver_extrato,
        "3":
        editar,
        "4":
        apagar,
    }

    while True:
        # ── Interface / Cabeçalho ─────────────────────────────
        limpar()
        print(
            "\n╔══════════════════════════╗"
            "\n║  💶  FinançasPro         ║"
            "\n╚══════════════════════════╝"
        )

        # ── Obter dados do utilizador ─────────────────────────
        id_rc    = get_id()
        nome_rc  = get_nome()
        saldo_rc = calcular_saldo()

        # ── Processar dados ─────────────────────
        id_val    = id_rc[1]    if id_rc[0] == 200 else "—"
        nome_val  = nome_rc[1]  if nome_rc[0] == 200 else "—"
        saldo_val = saldo_rc[1] if saldo_rc[0] == 200 else 0.0

        # ── Mostrar resumo ────────────────────────────────────
        print(f"  👤 {nome_val}  |  🆔 {id_val}  |  💰 {saldo_val:.2f}€  |  Trans: {len(transacoes)}\n")

        # ── Menu de opções ────────────────────────────────────
        sep()
        print("  1-Nova   2-Extrato   3-Editar   4-Apagar   0-Sair")
        sep()

        # ── Input ─────────────────────────────────────────────
        opcao = input("\n  Opção: ").strip()

        # ── Lógica do menu ────────────────────────────────────
        if opcao == "0":
            limpar()
            print(f"\n  👋 Até à próxima, {nome_val}!\n")
            break

        elif opcao in acoes:
            acoes[opcao]()   # executa a função correspondente

        else:
            print("  400 - Bad Request: Opção inválida.")
            time.sleep(1)

# ── Ponto de entrada ──────────────────────────────────────────

if __name__ == "__main__":
    limpar()
    if menu_auth():
        menu_principal()
