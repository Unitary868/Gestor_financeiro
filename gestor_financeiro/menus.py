# main.py – Interface, Login/Registo e ponto de entrada

import os, time
from transacao import (transacoes, adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes,
                       totais, escolher_cat)
from conta import (criar_conta, conta_existe, verificar_login,
                   get_nome, get_id, get_token)

# ── Funções UI ────────────────────────────────────────────────

def limpar():  os.system("cls" if os.name == "nt" else "clear")
def sep():     print("─" * 60)
def cab(t):    print("\n" + "═"*60 + f"\n  {t}\n" + "═"*60)
def pausar():  input("\n  Pressione Enter para continuar...")

def pedir_num(msg, mn=None, mx=None, dec=True):
    while True:
        try:
            v = (float if dec else int)(input(msg).strip().replace(",", "."))
            if (mn is None or v >= mn) and (mx is None or v <= mx):
                return v
            print(f"  ⚠  Intervalo: {mn} – {mx}")
        except ValueError:
            print("  ⚠  Número inválido.")

def pedir_texto(msg):
    while True:
        t = input(msg).strip()
        if t: return t
        print("  ⚠  Campo obrigatório.")

def pedir_nif():
    while True:
        n = input("  NIF (9 dígitos): ").strip()
        if n.isdigit() and len(n) == 9: return n
        print("  ⚠  NIF inválido! Deve ter 9 dígitos.")

def pedir_pin():
    while True:
        p = input("  PIN (4 dígitos): ").strip()
        if p.isdigit() and len(p) == 4: return p
        print("  ⚠  PIN inválido! Deve ter 4 dígitos.")

def pedir_password():
    while True:
        p = input("  Password (mín. 6 caracteres): ")
        if len(p) < 6: print("  ⚠  Password demasiado curta!"); continue
        c = input("  Confirmar password: ")
        if p == c: return p
        print("  ⚠  Passwords não coincidem!")

# ── Autenticação ──────────────────────────────────────────────

def registar():
    cab("📋 CRIAR CONTA")
    nome = pedir_texto("  Nome completo: ")
    nif  = pedir_nif()
    pin  = pedir_pin()
    _    = pedir_password()
    si   = pedir_num("  Saldo inicial (€): ", mn=0.0)
    uid, token = criar_conta(nome, nif, pin)
    if si > 0:
        adicionar_transacao("receita", "Saldo inicial", si, "Outros")
    sep()
    print(f"\n  ✅ Conta criada!\n  👤 {nome}  🆔 ID: {uid}  🔑 {token}  💰 {si:.2f}€")
    sep()
    pausar()

def login():
    cab("🔐 LOGIN")
    try:
        uid = int(input("  ID: ").strip())
    except ValueError:
        print("  ⚠  ID inválido."); pausar(); return False
    pin = input("  PIN: ").strip()
    if verificar_login(uid, pin):
        print(f"\n  ✅ Bem-vindo, {get_nome()}!")
        time.sleep(1)
        return True
    print("  ❌ ID ou PIN incorretos."); pausar(); return False

def menu_auth():
    while True:
        limpar()
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║          💶  FinançasPro - Gestor Financeiro             ║")
        print("╚══════════════════════════════════════════════════════════╝\n")
        sep(); print("  1 - Criar conta   2 - Entrar   0 - Sair"); sep()
        o = input("\n  Opção: ").strip()
        if o == "1":
            registar(); return True
        elif o == "2":
            if not conta_existe():
                print("  ⚠  Registe-se primeiro."); pausar()
            elif login():
                return True
        elif o == "0":
            limpar(); print("\n  👋 Até à próxima!\n"); return False
        else:
            print("  ⚠  Opção inválida."); time.sleep(1)

# ── Transações ────────────────────────────────────────────────

def nova_transacao():
    cab("NOVA TRANSAÇÃO")
    tipo = "receita" if int(pedir_num("  1-Receita  2-Despesa: ", 1, 2, False)) == 1 else "despesa"
    d    = pedir_texto("  Descrição: ")
    v    = pedir_num("  Valor (€): ", mn=0.01)
    c    = escolher_cat()
    idn  = adicionar_transacao(tipo, d, v, c)
    print(f"\n  ✅ #{idn} {'⬆' if tipo == 'receita' else '⬇'} {tipo.upper()} | {d} | {v:.2f}€")
    pausar()

def ver_extrato():
    cab("EXTRATO")
    if not transacoes:
        print("\n  Sem transações."); pausar(); return
    print("  1-Todas  2-Receitas  3-Despesas  4-Categoria")
    f   = int(pedir_num("  Filtro: ", 1, 4, False))
    lst = listar_transacoes(
        ["todas", "receitas", "despesas", "categoria"][f - 1],
        escolher_cat() if f == 4 else None
    )
    if not lst:
        print("\n  Sem resultados."); pausar(); return
    sep()
    print(f"  {'ID':<4} {'TIPO':<8} {'DESCRIÇÃO':<22} {'VALOR':>10}  CATEGORIA")
    sep()
    for t in lst:
        sg = "+" if t["tipo"] == "receita" else "-"
        print(f"  #{t['id']:<3} {'⬆' if t['tipo'] == 'receita' else '⬇'} {t['tipo']:<7} "
              f"{t['descricao']:<22} {sg}{t['valor']:>8.2f}€  {t['categoria']}")
    r, d = totais(lst)
    sep()
    print(f"  Receitas: +{r:.2f}€  Despesas: -{d:.2f}€")
    sep()
    pausar()

def editar():
    cab("EDITAR TRANSAÇÃO")
    if not transacoes:
        print("\n  Sem transações."); pausar(); return
    id_t = int(pedir_num("  ID: ", 1, dec=False))
    _, t = encontrar_transacao(id_t)
    if t is None:
        print(f"  ⚠  #{id_t} não encontrado."); pausar(); return
    print(f"\n  Atual → {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€ | {t['categoria']}")
    nd = input(f"  Descrição [{t['descricao']}]: ").strip()
    nv = None
    e  = input(f"  Valor [{t['valor']:.2f}]: ").strip().replace(",", ".")
    if e:
        try:
            nv = float(e) if float(e) > 0 else None
        except ValueError:
            pass
    nc = escolher_cat() if input("  Alterar categoria? (s/n): ").strip().lower() == "s" else None
    editar_transacao(id_t, nd or None, nv, nc)
    print(f"  ✅ #{id_t} atualizado.")
    pausar()

def apagar():
    cab("APAGAR TRANSAÇÃO")
    if not transacoes:
        print("\n  Sem transações."); pausar(); return
    id_t = int(pedir_num("  ID: ", 1, dec=False))
    _, t = encontrar_transacao(id_t)
    if t is None:
        print(f"  ⚠  #{id_t} não encontrado."); pausar(); return
    print(f"\n  {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€")
    if input("  Confirma? (s/n): ").strip().lower() == "s":
        apagar_transacao(id_t); print("  ✅ Apagado.")
    else:
        print("  ❌ Cancelado.")
    pausar()

# ── Menu Principal ────────────────────────────────────────────

def menu_principal():
    acoes = {
        "1": nova_transacao,
        "2": ver_extrato,
        "3": editar,
        "4": apagar,
    }
    while True:
        limpar()
        print(f"\n╔══════════════════════════╗\n║  💶  FinançasPro         ║\n╚══════════════════════════╝")
        print(f"  👤 {get_nome()}  |  🆔 {get_id()}  |  Trans: {len(transacoes)}\n")
        sep()
        print("  1-Nova   2-Extrato   3-Editar   4-Apagar   0-Sair")
        sep()
        o = input("\n  Opção: ").strip()
        if o == "0":
            limpar(); print(f"\n  👋 Até à próxima, {get_nome()}!\n"); break
        elif o in acoes:
            acoes[o]()
        else:
            print("  ⚠  Opção inválida."); time.sleep(1)

# ── Ponto de entrada ──────────────────────────────────────────

if __name__ == "__main__":
    limpar()
    if menu_auth():
        menu_principal()
