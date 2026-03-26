# menus.py – Interface, Login/Registo e main()

import time
from utils import limpar, sep, cab, pausar, pedir_num, pedir_texto, pedir_nif, pedir_pin, pedir_password, gerar_id, gerar_token
from entidades import (CATEGORIAS, transacoes, criar_conta, conta_existe, verificar_login,
                       get_nome, get_id, get_token, adicionar_transacao, encontrar_transacao,
                       editar_transacao, apagar_transacao, listar_transacoes, totais)
from operacoes import (EMPREGOS, metas, calcular_saldo, adicionar_meta, encontrar_meta,
                       atribuir_valor_meta, apagar_meta, percentagem_meta,
                       registar_trabalho, gastos_por_categoria)

# ── Helper ────────────────────────────────────────────────────

def escolher_cat():
    for i, c in enumerate(CATEGORIAS, 1): print(f"    {i:2}. {c}")
    return CATEGORIAS[int(pedir_num(f"  Categoria (1-{len(CATEGORIAS)}): ", 1, len(CATEGORIAS), False)) - 1]

# ── Autenticação ──────────────────────────────────────────────

def registar():
    cab("📋 CRIAR CONTA")
    nome = pedir_texto("  Nome completo: "); nif = pedir_nif()
    pin  = pedir_pin(); _ = pedir_password()
    si   = pedir_num("  Saldo inicial (€): ", mn=0.0)
    uid  = gerar_id(); token = gerar_token(uid)
    criar_conta(nome, nif, pin, uid, token)
    if si > 0: adicionar_transacao("receita", "Saldo inicial", si, "Outros")
    sep(); print(f"\n  ✅ Conta criada!\n  👤 {nome}  🆔 ID: {uid}  🔑 {token}  💰 {si:.2f}€"); sep(); pausar()

def login():
    cab("🔐 LOGIN")
    try: uid = int(input("  ID: ").strip())
    except ValueError: print("  ⚠  ID inválido."); pausar(); return False
    pin = input("  PIN: ").strip()
    if verificar_login(uid, pin): print(f"\n  ✅ Bem-vindo, {get_nome()}!"); time.sleep(1); return True
    print("  ❌ ID ou PIN incorretos."); pausar(); return False

def menu_auth():
    while True:
        limpar()
        print("\n╔══════════════════════════════════════════════════════════╗")
        print("║          💶  FinançasPro - Gestor Financeiro             ║")
        print("╚══════════════════════════════════════════════════════════╝\n")
        sep(); print("  1 - Criar conta   2 - Entrar   0 - Sair"); sep()
        o = input("\n  Opção: ").strip()
        if o == "1": registar(); return True
        elif o == "2":
            if not conta_existe(): print("  ⚠  Registe-se primeiro."); pausar()
            elif login(): return True
        elif o == "0": limpar(); print("\n  👋 Até à próxima!\n"); return False
        else: print("  ⚠  Opção inválida."); time.sleep(1)

# ── Transações ────────────────────────────────────────────────

def nova_transacao():
    cab("NOVA TRANSAÇÃO")
    tipo = "receita" if int(pedir_num("  1-Receita  2-Despesa: ", 1, 2, False)) == 1 else "despesa"
    d = pedir_texto("  Descrição: "); v = pedir_num("  Valor (€): ", mn=0.01); c = escolher_cat()
    idn = adicionar_transacao(tipo, d, v, c)
    print(f"\n  ✅ #{idn} {'⬆' if tipo=='receita' else '⬇'} {tipo.upper()} | {d} | {v:.2f}€\n  💰 Saldo: {calcular_saldo():.2f}€"); pausar()

def ver_extrato():
    cab("EXTRATO")
    if not transacoes: print("\n  Sem transações."); pausar(); return
    print("  1-Todas  2-Receitas  3-Despesas  4-Categoria")
    f = int(pedir_num("  Filtro: ", 1, 4, False))
    lst = listar_transacoes(["todas","receitas","despesas","categoria"][f-1], escolher_cat() if f==4 else None)
    if not lst: print("\n  Sem resultados."); pausar(); return
    sep(); print(f"  {'ID':<4} {'TIPO':<8} {'DESCRIÇÃO':<22} {'VALOR':>10}  CATEGORIA"); sep()
    for t in lst:
        sg = "+" if t["tipo"]=="receita" else "-"
        print(f"  #{t['id']:<3} {'⬆' if t['tipo']=='receita' else '⬇'} {t['tipo']:<7} {t['descricao']:<22} {sg}{t['valor']:>8.2f}€  {t['categoria']}")
    r, d = totais(lst); sep(); print(f"  Receitas: +{r:.2f}€  Despesas: -{d:.2f}€  Saldo: {calcular_saldo():.2f}€"); sep(); pausar()

def editar():
    cab("EDITAR TRANSAÇÃO")
    if not transacoes: print("\n  Sem transações."); pausar(); return
    id_t = int(pedir_num("  ID: ", 1, dec=False)); _, t = encontrar_transacao(id_t)
    if t is None: print(f"  ⚠  #{id_t} não encontrado."); pausar(); return
    print(f"\n  Atual → {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€ | {t['categoria']}")
    nd = input(f"  Descrição [{t['descricao']}]: ").strip()
    nv = None; e = input(f"  Valor [{t['valor']:.2f}]: ").strip().replace(",",".")
    if e:
        try: nv = float(e) if float(e) > 0 else None
        except: pass
    nc = escolher_cat() if input("  Alterar categoria? (s/n): ").strip().lower()=="s" else None
    editar_transacao(id_t, nd or None, nv, nc); print(f"  ✅ #{id_t} atualizado."); pausar()

def apagar():
    cab("APAGAR TRANSAÇÃO")
    if not transacoes: print("\n  Sem transações."); pausar(); return
    id_t = int(pedir_num("  ID: ", 1, dec=False)); _, t = encontrar_transacao(id_t)
    if t is None: print(f"  ⚠  #{id_t} não encontrado."); pausar(); return
    print(f"\n  {t['tipo']} | {t['descricao']} | {t['valor']:.2f}€")
    if input("  Confirma? (s/n): ").strip().lower()=="s":
        apagar_transacao(id_t); print(f"  ✅ Apagado. Saldo: {calcular_saldo():.2f}€")
    else: print("  ❌ Cancelado.")
    pausar()

# ── Metas ─────────────────────────────────────────────────────

def menu_metas():
    while True:
        cab("🎯 METAS"); print(f"\n  💰 Saldo: {calcular_saldo():.2f}€\n")
        print("  1-Ver  2-Criar  3-Atribuir  4-Apagar  0-Voltar")
        o = input("\n  Opção: ").strip()
        if o == "1":
            cab("METAS"); sep()
            if not metas: print("  Sem metas.")
            for m in metas:
                p = percentagem_meta(m); b = "█"*int(p/5)+"░"*(20-int(p/5))
                print(f"  #{m['id']} {m['nome']:<20} {m['atual']:.2f}€/{m['objetivo']:.2f}€\n  [{b}] {p:.1f}%{' ✅' if p>=100 else ''}\n")
            sep(); pausar()
        elif o == "2":
            cab("NOVA META"); n = pedir_texto("  Nome: "); obj = pedir_num("  Objetivo (€): ", mn=0.01)
            print(f"  ✅ Meta #{adicionar_meta(n, obj)} '{n}' criada!"); pausar()
        elif o == "3":
            cab("ATRIBUIR"); sl = calcular_saldo()
            if not metas or sl <= 0: print(f"  ⚠  {'Sem metas.' if not metas else f'Saldo: {sl:.2f}€'}"); pausar(); continue
            for m in metas: print(f"  #{m['id']} {m['nome']} ({m['atual']:.2f}€/{m['objetivo']:.2f}€)")
            id_m = int(pedir_num("\n  ID da meta: ", 1, dec=False)); _, m = encontrar_meta(id_m)
            if m is None: print("  ⚠  Não encontrada."); pausar(); continue
            v = pedir_num(f"  Montante (máx {sl:.2f}€): ", 0.01, sl)
            atribuir_valor_meta(id_m, v); _, ma = encontrar_meta(id_m); p = percentagem_meta(ma)
            print(f"  ✅ {v:.2f}€ → '{m['nome']}' ({p:.1f}%){'  🎉 Meta atingida!' if p>=100 else ''}"); pausar()
        elif o == "4":
            cab("APAGAR META")
            if not metas: print("  Sem metas."); pausar(); continue
            for m in metas: print(f"  #{m['id']} {m['nome']}")
            id_m = int(pedir_num("\n  ID: ", 1, dec=False)); _, m = encontrar_meta(id_m)
            if m is None: print("  ⚠  Não encontrada."); pausar(); continue
            if input(f"  Apagar '{m['nome']}'? (s/n): ").strip().lower()=="s":
                apagar_meta(id_m); print("  ✅ Apagada.")
            else: print("  ❌ Cancelado.")
            pausar()
        elif o == "0": break

# ── Emprego ───────────────────────────────────────────────────

def menu_emprego():
    cab("💼 TRABALHAR"); print(f"\n  💰 Saldo: {calcular_saldo():.2f}€\n")
    sep(); print(f"  {'Nº':<4} {'PROFISSÃO':<22} {'€/h':>6}  {'h':>4}  {'GANHO':>9}"); sep()
    for i, (n, eh, h) in enumerate(EMPREGOS, 1): print(f"  {i:<4} {n:<22} {eh:>5.2f}€  {h:>3}h  {eh*h:>8.2f}€")
    sep(); print("  0 - Voltar")
    e = int(pedir_num(f"\n  Emprego (0-{len(EMPREGOS)}): ", 0, len(EMPREGOS), False))
    if e == 0: return
    print(f"\n  🏢 A trabalhar como {EMPREGOS[e-1][0]}..."); time.sleep(1)
    g = registar_trabalho(e - 1); print(f"\n  ✅ Ganhou {g:.2f}€  |  💰 Saldo: {calcular_saldo():.2f}€"); pausar()

# ── Resumo ────────────────────────────────────────────────────

def resumo():
    cab("📊 RESUMO"); sl = calcular_saldo(); r, d = totais(transacoes)
    print(f"\n  👤 {get_nome()}  🆔 {get_id()}  🔑 {get_token()}")
    print(f"\n  📥 +{r:.2f}€   📤 -{d:.2f}€   💰 {sl:.2f}€")
    print(f"  Situação: {'🟢 POSITIVA' if sl>0 else '🟡 NEUTRA' if sl==0 else '🔴 NEGATIVA'}")
    gc = gastos_por_categoria()
    if gc:
        sep(); mx = max(gc.values())
        for c, v in gc.items():
            b = "█"*int(v/mx*20)+"░"*(20-int(v/mx*20)); print(f"  {c:<15} [{b}] {v:.2f}€")
    if metas:
        sep()
        for m in metas:
            p = percentagem_meta(m); print(f"  🎯 {m['nome']:<20} {m['atual']:.2f}€/{m['objetivo']:.2f}€  [{'✅' if p>=100 else f'{p:.1f}%'}]")
    sep(); print(f"  Transações: {len(transacoes)}  |  Metas: {len(metas)}"); pausar()

# ── Menu Principal ────────────────────────────────────────────

def menu_principal():
    acoes = {"1": nova_transacao, "2": ver_extrato, "3": editar,
             "4": apagar, "5": menu_metas, "6": menu_emprego, "7": resumo}
    while True:
        limpar(); sl = calcular_saldo()
        print(f"\n╔══════════════════════════╗\n║  💶  FinançasPro         ║\n╚══════════════════════════╝")
        print(f"  👤 {get_nome()}  |  💰 {sl:.2f}€  |  Trans: {len(transacoes)}  |  Metas: {len(metas)}\n")
        sep(); print("  1-Nova   2-Extrato   3-Editar   4-Apagar"); print("  5-🎯 Metas   6-💼 Trabalhar   7-📊 Resumo   0-Sair"); sep()
        o = input("\n  Opção: ").strip()
        if o == "0": limpar(); print(f"\n  👋 Até à próxima, {get_nome()}!\n"); break
        elif o in acoes: acoes[o]()
        else: print("  ⚠  Opção inválida."); time.sleep(1)

def main():
    limpar()
    if menu_auth(): menu_principal()

if __name__ == "__main__":
    main()
