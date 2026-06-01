# app.py — Gestão Financeira | Tkinter
# Estrutura funcional — sem classes, variáveis globais

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from logger import get_logger

from conta import (
    criar_conta, listar_contas, consultar_conta,
    atualizar_pin, eliminar_conta, verificar_login,
)
from transacao import (
    adicionar_transacao, listar_transacoes, encontrar_transacao,
    editar_transacao, apagar_transacao, calcular_saldo, totais,
)
from orcamento import (
    criar_orcamento, listar_orcamentos, consultar_orcamento,
    atualizar_orcamento, remover_orcamento, registar_gasto,
)
from pagamento import (
    criar_pagamento, listar_pagamentos, consultar_pagamento,
    atualizar_pagamento, remover_pagamento,
)

log = get_logger("app")


# ══════════════════════════════════════════════════════════════
# CONSTANTES
# ══════════════════════════════════════════════════════════════

CATEGORIAS_TRANSACAO = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Salário", "Freelance", "Outros",
)
CATEGORIAS_ORCAMENTO = (
    "Alimentação", "Transporte", "Lazer", "Saúde",
    "Educação", "Habitação", "Vestuário", "Tecnologia",
    "Poupança", "Outros",
)
PERIODOS    = ("diário", "semanal", "mensal", "anual")
METODOS_PAG = ("MB Way", "Transferência", "Multibanco", "Dinheiro", "Cartão")

C_DARK    = "#1a1a2e"
C_ACCENT  = "#e94560"
C_BG      = "#f4f6f8"
C_FRAME   = "#ffffff"
C_TEXTO   = "#2d3436"
C_MUTED   = "#636e72"
C_SUCCESS = "#00b894"
C_ERROR   = "#d63031"
C_WARN    = "#fdcb6e"

BTN_CORES = {
    "criar":     ("#27ae60", "#2ecc71"),
    "consultar": ("#2980b9", "#3498db"),
    "atualizar": ("#d35400", "#e67e22"),
    "remover":   ("#c0392b", "#e74c3c"),
    "limpar":    ("#636e72", "#7f8c8d"),
    "login":     ("#1a1a2e", "#2d3436"),
    "registar":  ("#6c5ce7", "#a29bfe"),
    "voltar":    ("#b2bec3", "#636e72"),
}

F_NORMAL = ("Helvetica", 10)
F_BOLD   = ("Helvetica", 10, "bold")
F_TITULO = ("Helvetica", 12, "bold")
F_GRANDE = ("Helvetica", 16, "bold")
F_BTN    = ("Helvetica", 9,  "bold")
F_SMALL  = ("Helvetica", 9)
F_TABELA = ("Helvetica", 9)

# conta autenticada (preenchida após login)
conta_atual = {}


# ══════════════════════════════════════════════════════════════
# ESTILOS
# ══════════════════════════════════════════════════════════════

def aplicar_estilos():
    s = ttk.Style(janela)
    s.theme_use("clam")
    s.configure("TNotebook",          background=C_BG, borderwidth=0)
    s.configure("TNotebook.Tab",      font=F_BOLD, padding=[16, 8],
                                       background="#dfe6e9", foreground=C_MUTED)
    s.map("TNotebook.Tab",
          background=[("selected", C_FRAME)],
          foreground=[("selected", C_ACCENT)])
    s.configure("TFrame",             background=C_BG)
    s.configure("Tabela.Treeview",    font=F_TABELA, rowheight=26,
                                       background=C_FRAME, fieldbackground=C_FRAME,
                                       foreground=C_TEXTO)
    s.configure("Tabela.Treeview.Heading",
                                       font=("Helvetica", 9, "bold"),
                                       background="#dfe6e9", foreground=C_TEXTO, relief="flat")
    s.map("Tabela.Treeview",          background=[("selected", "#2980b9")],
                                       foreground=[("selected", "white")])
    s.configure("TScrollbar",         background="#dfe6e9", troughcolor=C_BG,
                                       borderwidth=0, arrowsize=12)
    s.configure("TCombobox",          padding=4)


# ══════════════════════════════════════════════════════════════
# WIDGETS AUXILIARES
# ══════════════════════════════════════════════════════════════

def btn(parent, texto, cmd, tipo, width=12):
    bg, active = BTN_CORES[tipo]
    b = tk.Button(parent, text=texto, command=cmd, width=width,
                  bg=bg, fg="white", activebackground=active, activeforeground="white",
                  font=F_BTN, relief="flat", cursor="hand2", pady=5)
    b.bind("<Enter>", lambda e: b.config(bg=active))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def campo(frame, texto, row, col=0, show=None, readonly=False, width=24):
    tk.Label(frame, text=texto, font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO, anchor="e"
             ).grid(row=row, column=col * 2, sticky="e", padx=(12, 6), pady=5)
    e = tk.Entry(frame, width=width, show=show or "",
                 state="readonly" if readonly else "normal",
                 relief="solid", bd=1, font=F_NORMAL, bg="white")
    e.grid(row=row, column=col * 2 + 1, sticky="w", padx=(0, 16), pady=5)
    return e


def combo(frame, texto, row, values, col=0, width=22):
    tk.Label(frame, text=texto, font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO, anchor="e"
             ).grid(row=row, column=col * 2, sticky="e", padx=(12, 6), pady=5)
    c = ttk.Combobox(frame, values=values, width=width, state="readonly", font=F_NORMAL)
    c.grid(row=row, column=col * 2 + 1, sticky="w", padx=(0, 16), pady=5)
    return c


def treeview(frame, colunas, larguras=None):
    tree = ttk.Treeview(frame, columns=colunas, show="headings",
                        height=12, style="Tabela.Treeview", selectmode="browse")
    for i, col in enumerate(colunas):
        tree.heading(col, text=col)
        tree.column(col, width=larguras[i] if larguras else 150, anchor="center")
    tree.tag_configure("par",      background="#f8f9fa")
    tree.tag_configure("impar",    background=C_FRAME)
    tree.tag_configure("excedido", background="#ffe0e0", foreground="#c0392b")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    return tree


def linha(tree, valores, tag_extra=None):
    n   = len(tree.get_children())
    tag = tag_extra or ("par" if n % 2 == 0 else "impar")
    tree.insert("", tk.END, values=valores, tags=(tag,))


def limpar_tree(tree):
    tree.delete(*tree.get_children())


def set_entry(entry, valor, readonly=False):
    if readonly:
        entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, str(valor) if valor else "")
    if readonly:
        entry.config(state="readonly")


def limpar_widgets(*widgets):
    for w in widgets:
        if isinstance(w, ttk.Combobox):
            w.set("")
        elif w.cget("state") == "readonly":
            w.config(state="normal")
            w.delete(0, tk.END)
            w.config(state="readonly")
        else:
            w.delete(0, tk.END)


def erro_inline(label, msg, after_ms=4000):
    label.config(text=msg, fg=C_ERROR)
    if after_ms:
        label.after(after_ms, lambda: label.config(text=""))


def msg_inline(label, txt, cor, after_ms=5000):
    label.config(text=txt, fg=cor)
    label.after(after_ms, lambda: label.config(text=""))


def lf(parent, titulo, fill=tk.X, expand=False, pady=(10, 4)):
    f = tk.LabelFrame(parent, text=f"  {titulo}  ", font=F_TITULO,
                      bg=C_FRAME, fg=C_TEXTO, relief="solid", bd=1)
    f.pack(fill=fill, expand=expand, padx=16, pady=pady)
    return f


def set_status(msg, tipo="ok"):
    cores = {"ok": C_SUCCESS, "erro": C_ERROR, "aviso": C_WARN}
    st_icon.config(fg=cores.get(tipo, C_SUCCESS))
    st_var.set(f"  {msg}")


# ══════════════════════════════════════════════════════════════
# NAVEGAÇÃO ENTRE FRAMES
# ══════════════════════════════════════════════════════════════

frame_atual = None


def mostrar_frame(novo_frame):
    global frame_atual
    if frame_atual:
        frame_atual.pack_forget()
    novo_frame.pack(fill=tk.BOTH, expand=True)
    frame_atual = novo_frame


# ══════════════════════════════════════════════════════════════
# LOGIN — construção
# ══════════════════════════════════════════════════════════════

def construir_login():
    global frame_login, card_login
    global e_login_id, e_login_pin, lbl_err_login
    global e_reg_nome, e_reg_nif, e_reg_pin, lbl_err_reg
    global v_login, v_reg

    frame_login = tk.Frame(janela, bg=C_DARK)

    card_login = tk.Frame(frame_login, bg=C_FRAME)
    card_login.place(relx=.5, rely=.5, anchor="center", width=400, height=500)
    tk.Frame(card_login, bg=C_ACCENT, height=6).pack(fill=tk.X)

    # ── vista login ───────────────────────────────────────────
    v_login = tk.Frame(card_login, bg=C_FRAME)

    tk.Label(v_login, text="💰", font=("Helvetica", 36), bg=C_FRAME).pack(pady=(24, 4))
    tk.Label(v_login, text="Gestão Financeira", font=F_GRANDE, bg=C_FRAME, fg=C_DARK).pack()
    tk.Label(v_login, text="Inicie sessão para continuar", font=F_SMALL,
             bg=C_FRAME, fg=C_MUTED).pack(pady=(3, 18))
    ttk.Separator(v_login).pack(fill=tk.X, padx=28, pady=(0, 12))

    frm_l = tk.Frame(v_login, bg=C_FRAME)
    frm_l.pack(padx=30, fill=tk.X)

    tk.Label(frm_l, text="ID da Conta", font=F_BOLD, bg=C_FRAME, anchor="w").pack(fill=tk.X)
    e_login_id = tk.Entry(frm_l, font=F_NORMAL, relief="solid", bd=1)
    e_login_id.pack(fill=tk.X, ipady=6, pady=(3, 12))

    tk.Label(frm_l, text="PIN", font=F_BOLD, bg=C_FRAME, anchor="w").pack(fill=tk.X)
    e_login_pin = tk.Entry(frm_l, font=F_NORMAL, relief="solid", bd=1, show="*")
    e_login_pin.pack(fill=tk.X, ipady=6, pady=(3, 4))
    e_login_pin.bind("<Return>", lambda _: fazer_login())

    lbl_err_login = tk.Label(frm_l, text="", font=F_SMALL, bg=C_FRAME, fg=C_ERROR)
    lbl_err_login.pack(fill=tk.X, pady=(0, 6))

    frm_lb = tk.Frame(v_login, bg=C_FRAME)
    frm_lb.pack(padx=30, fill=tk.X)
    btn(frm_lb, "Entrar",      fazer_login,          "login",    width=16).pack(fill=tk.X, ipady=3, pady=(2, 6))
    btn(frm_lb, "Criar Conta", mostrar_registo,      "registar", width=16).pack(fill=tk.X, ipady=3)

    # ── vista registo ─────────────────────────────────────────
    v_reg = tk.Frame(card_login, bg=C_FRAME)

    tk.Label(v_reg, text="Nova Conta", font=F_TITULO, bg=C_FRAME, fg=C_DARK).pack(pady=(24, 4))
    tk.Label(v_reg, text="Preencha os dados abaixo", font=F_SMALL,
             bg=C_FRAME, fg=C_MUTED).pack(pady=(0, 14))
    ttk.Separator(v_reg).pack(fill=tk.X, padx=28, pady=(0, 10))

    frm_r = tk.Frame(v_reg, bg=C_FRAME)
    frm_r.pack(padx=30, fill=tk.X)

    tk.Label(frm_r, text="Nome completo",  font=F_BOLD, bg=C_FRAME, anchor="w").pack(fill=tk.X)
    e_reg_nome = tk.Entry(frm_r, font=F_NORMAL, relief="solid", bd=1)
    e_reg_nome.pack(fill=tk.X, ipady=5, pady=(3, 10))

    tk.Label(frm_r, text="NIF (9 dígitos)", font=F_BOLD, bg=C_FRAME, anchor="w").pack(fill=tk.X)
    e_reg_nif = tk.Entry(frm_r, font=F_NORMAL, relief="solid", bd=1)
    e_reg_nif.pack(fill=tk.X, ipady=5, pady=(3, 10))

    tk.Label(frm_r, text="PIN (4 dígitos)", font=F_BOLD, bg=C_FRAME, anchor="w").pack(fill=tk.X)
    e_reg_pin = tk.Entry(frm_r, font=F_NORMAL, relief="solid", bd=1, show="*")
    e_reg_pin.pack(fill=tk.X, ipady=5, pady=(3, 4))
    e_reg_pin.bind("<Return>", lambda _: registar_conta())

    lbl_err_reg = tk.Label(frm_r, text="", font=F_SMALL, bg=C_FRAME, fg=C_ERROR)
    lbl_err_reg.pack(fill=tk.X, pady=(0, 6))

    frm_rb = tk.Frame(v_reg, bg=C_FRAME)
    frm_rb.pack(padx=30, fill=tk.X)
    btn(frm_rb, "Criar Conta", registar_conta,  "criar",  width=16).pack(fill=tk.X, ipady=3, pady=(2, 6))
    btn(frm_rb, "← Voltar",   mostrar_login_v, "voltar", width=16).pack(fill=tk.X, ipady=3)

    mostrar_login_v()


def mostrar_login_v():
    v_reg.pack_forget()
    v_login.pack(fill=tk.BOTH, expand=True)
    e_login_id.focus()


def mostrar_registo():
    v_login.pack_forget()
    v_reg.pack(fill=tk.BOTH, expand=True)
    e_reg_nome.focus()


# ── ações login ───────────────────────────────────────────────

def fazer_login():
    uid = e_login_id.get().strip()
    pin = e_login_pin.get().strip()
    if not uid or not pin:
        return erro_inline(lbl_err_login, "Preencha o ID e o PIN.")
    log.info("AUTH login | id=%s", uid)
    code, obj = verificar_login(uid, pin)
    if code == 200:
        log.info("AUTH ok | id=%s | nome=%s", uid, obj["nome"])
        conta_atual.update(obj)
        abrir_app()
    else:
        log.error("AUTH falhou | id=%s | %s", uid, obj)
        erro_inline(lbl_err_login, str(obj))


def registar_conta():
    nome = e_reg_nome.get().strip()
    if not nome:
        return erro_inline(lbl_err_reg, "400: Nome obrigatório.")
    code, obj = criar_conta(nome, e_reg_nif.get().strip(), e_reg_pin.get().strip())
    if code == 201:
        log.info("AUTH conta criada | id=%s", obj["id"])
        limpar_widgets(e_reg_nome, e_reg_nif, e_reg_pin)
        lbl_err_reg.config(text="")
        mostrar_login_v()
        e_login_id.delete(0, tk.END)
        e_login_id.insert(0, obj["id"])
        lbl_err_login.config(text=f"✓ Conta criada! ID: {obj['id']} — faça login.", fg=C_SUCCESS)
        lbl_err_login.after(8000, lambda: lbl_err_login.config(text=""))
    else:
        log.error("AUTH criar conta | %s", obj)
        erro_inline(lbl_err_reg, str(obj))


# ══════════════════════════════════════════════════════════════
# MAIN APP — construção
# ══════════════════════════════════════════════════════════════

def construir_app():
    global frame_app, lbl_hora, st_icon, st_var
    global notebook

    frame_app = tk.Frame(janela, bg=C_BG)

    # ── header ────────────────────────────────────────────────
    hdr = tk.Frame(frame_app, bg=C_DARK, height=56)
    hdr.pack(fill=tk.X)
    hdr.pack_propagate(False)

    tk.Label(hdr, text="💰  Gestão Financeira",
             bg=C_DARK, fg="white", font=("Helvetica", 14, "bold")
             ).pack(side=tk.LEFT, padx=20, pady=14)

    tk.Button(hdr, text="⎋  Sair", command=fazer_logout,
              bg=C_ACCENT, fg="white", relief="flat",
              font=F_BTN, cursor="hand2", padx=12, pady=6
              ).pack(side=tk.RIGHT, padx=16, pady=10)

    lbl_usuario = tk.Label(hdr, text="", bg=C_DARK, fg="#a0aec0", font=F_SMALL)
    lbl_usuario.pack(side=tk.RIGHT, padx=4)

    lbl_hora = tk.Label(hdr, text="", bg=C_DARK, fg="#636e72", font=F_SMALL)
    lbl_hora.pack(side=tk.RIGHT, padx=16)

    # guarda referência para atualizar o nome após login
    frame_app._lbl_usuario = lbl_usuario

    # ── notebook ──────────────────────────────────────────────
    notebook = ttk.Notebook(frame_app)
    notebook.pack(fill=tk.BOTH, expand=True)

    construir_tab_conta()
    construir_tab_transacoes()
    construir_tab_orcamentos()
    construir_tab_pagamentos()

    # ── status bar ────────────────────────────────────────────
    bar = tk.Frame(frame_app, bg="#2d3436", height=30)
    bar.pack(fill=tk.X, side=tk.BOTTOM)
    bar.pack_propagate(False)

    st_icon = tk.Label(bar, text="●", bg="#2d3436", fg=C_SUCCESS, font=("Helvetica", 11))
    st_icon.pack(side=tk.LEFT, padx=(12, 4), pady=5)

    st_var = tk.StringVar(value="Pronto.")
    tk.Label(bar, textvariable=st_var, bg="#2d3436",
             fg="#dfe6e9", font=F_SMALL, anchor="w").pack(side=tk.LEFT)

    tk.Label(bar, text="Gestão Financeira  v1.0",
             bg="#2d3436", fg="#636e72", font=("Helvetica", 8)).pack(side=tk.RIGHT, padx=12)


def tick():
    lbl_hora.config(text=datetime.now().strftime("%d/%m/%Y  %H:%M:%S"))
    janela.after(1000, tick)


def fazer_logout():
    if messagebox.askyesno("Logout", "Tem a certeza que pretende sair?"):
        log.info("AUTH logout | id=%s", conta_atual.get("id"))
        conta_atual.clear()
        mostrar_frame(frame_login)
        mostrar_login_v()
        e_login_id.delete(0, tk.END)
        e_login_pin.delete(0, tk.END)


def abrir_app():
    frame_app._lbl_usuario.config(text=f"👤  {conta_atual['nome']}")
    # recarregar dados nas tabs
    carregar_tabela_transacoes()
    carregar_tabela_orcamentos()
    carregar_tabela_pagamentos()
    atualizar_saldo()
    # atualizar campo id_conta nas transações
    set_entry(e_trans_id_conta, conta_atual["id"], readonly=True)
    # atualizar info da conta
    lbl_conta_id.config(text=conta_atual["id"])
    lbl_conta_nome.config(text=conta_atual["nome"])
    lbl_conta_nif.config(text=conta_atual["nif"])
    mostrar_frame(frame_app)
    tick()


# ══════════════════════════════════════════════════════════════
# TAB — MINHA CONTA
# ══════════════════════════════════════════════════════════════

def construir_tab_conta():
    global lbl_conta_id, lbl_conta_nome, lbl_conta_nif
    global lbl_saldo, lbl_receitas, lbl_despesas
    global e_pin_atual, e_pin_novo, lbl_pin_msg
    global e_pin_elim, lbl_del_msg

    tab = tk.Frame(notebook, bg=C_BG)
    notebook.add(tab, text="  Minha Conta  ")

    # ── Informações ───────────────────────────────────────────
    frm_info = lf(tab, "Informações da Conta")
    for i, (rotulo, var_name) in enumerate([("ID", "id"), ("Nome", "nome"), ("NIF", "nif")]):
        tk.Label(frm_info, text=f"{rotulo}:", font=F_BOLD, bg=C_FRAME, fg=C_MUTED
                 ).grid(row=i, column=0, sticky="e", padx=(20, 8), pady=5)

    lbl_conta_id   = tk.Label(frm_info, text="", font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO)
    lbl_conta_nome = tk.Label(frm_info, text="", font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO)
    lbl_conta_nif  = tk.Label(frm_info, text="", font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO)
    lbl_conta_id.grid(  row=0, column=1, sticky="w")
    lbl_conta_nome.grid(row=1, column=1, sticky="w")
    lbl_conta_nif.grid( row=2, column=1, sticky="w")

    # ── Resumo financeiro ─────────────────────────────────────
    frm_s = lf(tab, "Resumo Financeiro")

    lbl_saldo    = tk.Label(frm_s, text="0.00€", font=("Helvetica", 22, "bold"), bg=C_FRAME, fg=C_SUCCESS)
    lbl_receitas = tk.Label(frm_s, text="▲ 0.00€", font=F_BOLD, bg=C_FRAME, fg=C_SUCCESS)
    lbl_despesas = tk.Label(frm_s, text="▼ 0.00€", font=F_BOLD, bg=C_FRAME, fg=C_ERROR)

    for i, (rotulo, widget) in enumerate([("Saldo atual:", lbl_saldo),
                                           ("Receitas:",   lbl_receitas),
                                           ("Despesas:",   lbl_despesas)]):
        tk.Label(frm_s, text=rotulo, font=F_BOLD, bg=C_FRAME, fg=C_MUTED
                 ).grid(row=i, column=0, sticky="e", padx=(20, 8), pady=4)
        widget.grid(row=i, column=1, sticky="w")

    tk.Button(frm_s, text="↻  Atualizar Saldo", font=F_BTN, command=atualizar_saldo,
              bg="#dfe6e9", fg=C_TEXTO, relief="flat", cursor="hand2", padx=8
              ).grid(row=3, column=0, columnspan=2, pady=(8, 6))

    # ── Alterar PIN ───────────────────────────────────────────
    frm_pin = lf(tab, "Alterar PIN")
    fi = tk.Frame(frm_pin, bg=C_FRAME)
    fi.pack(padx=12, pady=8, fill=tk.X)

    tk.Label(fi, text="PIN atual:",  font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO
             ).grid(row=0, column=0, sticky="e", padx=(0, 6), pady=4)
    e_pin_atual = tk.Entry(fi, width=14, show="*", relief="solid", bd=1, font=F_NORMAL)
    e_pin_atual.grid(row=0, column=1, sticky="w", padx=(0, 20))

    tk.Label(fi, text="Novo PIN:", font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO
             ).grid(row=0, column=2, sticky="e", padx=(0, 6))
    e_pin_novo = tk.Entry(fi, width=14, show="*", relief="solid", bd=1, font=F_NORMAL)
    e_pin_novo.grid(row=0, column=3, sticky="w", padx=(0, 12))

    lbl_pin_msg = tk.Label(fi, text="", font=F_SMALL, bg=C_FRAME)
    lbl_pin_msg.grid(row=1, column=0, columnspan=4, sticky="w", pady=(2, 0))

    btn(fi, "Guardar PIN", alterar_pin, "atualizar", width=14).grid(row=0, column=4, padx=(8, 0))

    # ── Zona de Perigo ────────────────────────────────────────
    frm_del = lf(tab, "Zona de Perigo")
    fd = tk.Frame(frm_del, bg=C_FRAME)
    fd.pack(padx=12, pady=8, fill=tk.X)

    tk.Label(fd, text="PIN de confirmação:", font=F_NORMAL, bg=C_FRAME, fg=C_TEXTO
             ).grid(row=0, column=0, sticky="e", padx=(0, 6), pady=4)
    e_pin_elim = tk.Entry(fd, width=14, show="*", relief="solid", bd=1, font=F_NORMAL)
    e_pin_elim.grid(row=0, column=1, sticky="w", padx=(0, 12))

    lbl_del_msg = tk.Label(fd, text="", font=F_SMALL, bg=C_FRAME)
    lbl_del_msg.grid(row=1, column=0, columnspan=3, sticky="w", pady=(2, 0))

    btn(fd, "Eliminar Conta", eliminar_conta_ui, "remover", width=14).grid(row=0, column=2, padx=(8, 0))


def atualizar_saldo():
    if not conta_atual:
        return
    _, saldo     = calcular_saldo(conta_atual["id"])
    _, rec, desp = totais(conta_atual["id"])
    cor = C_SUCCESS if saldo >= 0 else C_ERROR
    lbl_saldo.config(text=f"{saldo:.2f}€", fg=cor)
    lbl_receitas.config(text=f"▲ {rec:.2f}€")
    lbl_despesas.config(text=f"▼ {desp:.2f}€")
    set_status("Saldo atualizado.")
    log.info("Saldo atualizado")


def alterar_pin():
    p_atual = e_pin_atual.get().strip()
    p_novo  = e_pin_novo.get().strip()
    if not p_atual or not p_novo:
        lbl_pin_msg.config(text="Preencha os dois campos.", fg=C_WARN)
        return
    code, obj = atualizar_pin(conta_atual["id"], p_atual, p_novo)
    if code == 200:
        conta_atual["pin"] = p_novo
        limpar_widgets(e_pin_atual, e_pin_novo)
        lbl_pin_msg.config(text="✓ PIN atualizado.", fg=C_SUCCESS)
        set_status("PIN atualizado com sucesso.")
        log.info("PIN atualizado")
    else:
        lbl_pin_msg.config(text=str(obj), fg=C_ERROR)
        log.error("PIN falhou | %s", obj)


def eliminar_conta_ui():
    pin = e_pin_elim.get().strip()
    if not pin:
        lbl_del_msg.config(text="Insira o PIN de confirmação.", fg=C_WARN)
        return
    if not messagebox.askyesno("Confirmação", "Esta ação é irreversível.\nTem a certeza que pretende eliminar a sua conta?"):
        return
    code, obj = eliminar_conta(conta_atual["id"], pin)
    if code == 200:
        set_status(f"Conta eliminada → {conta_atual['id']}")
        log.info("Conta eliminada | id=%s", conta_atual["id"])
        messagebox.showinfo("Eliminada", "Conta eliminada. A aplicação vai fechar.")
        janela.destroy()
    else:
        lbl_del_msg.config(text=str(obj), fg=C_ERROR)
        log.error("Eliminar conta falhou | %s", obj)


# ══════════════════════════════════════════════════════════════
# TAB — TRANSAÇÕES
# ══════════════════════════════════════════════════════════════

def construir_tab_transacoes():
    global e_trans_id, cb_trans_tipo, e_trans_descricao, e_trans_valor
    global cb_trans_cat, e_trans_id_orc, e_trans_id_conta
    global e_trans_data_pag, cb_trans_metodo_pag
    global tabela_transacoes, lbl_msg_trans

    tab = tk.Frame(notebook, bg=C_BG)
    notebook.add(tab, text="  Transações  ")

    frm = lf(tab, "Formulário — Transação")

    e_trans_id        = campo(frm, "ID",           0, col=0, readonly=True)
    cb_trans_tipo     = combo(frm, "Tipo",         1, col=0, values=("receita", "despesa"))
    e_trans_descricao = campo(frm, "Descrição",    2, col=0)
    e_trans_valor     = campo(frm, "Valor (€)",    3, col=0)

    cb_trans_cat        = combo(frm, "Categoria",         0, col=1, values=CATEGORIAS_TRANSACAO)
    e_trans_id_orc      = campo(frm, "ID Orçamento",      1, col=1)
    e_trans_data_pag    = campo(frm, "Data Pagamento",    2, col=1)
    cb_trans_metodo_pag = combo(frm, "Método Pagamento", 3, col=1, values=METODOS_PAG)

    set_entry(e_trans_data_pag, datetime.now().strftime("%Y-%m-%d"))

    tk.Label(frm, text="ID Conta", font=F_NORMAL, bg=C_FRAME, fg=C_MUTED, anchor="e"
             ).grid(row=4, column=0, sticky="e", padx=(12, 6), pady=5)
    e_trans_id_conta = tk.Entry(frm, width=24, font=F_NORMAL, state="readonly",
                                relief="solid", bd=1, bg="#f0f0f0")
    e_trans_id_conta.grid(row=4, column=1, sticky="w", padx=(0, 16), pady=5)

    frm_btn = tk.Frame(tab, bg=C_BG)
    frm_btn.pack(pady=8)
    for txt, cmd, tipo in [
        ("Adicionar", adicionar_transacao_ui, "criar"),
        ("Consultar", consultar_transacao,    "consultar"),
        ("Editar",    editar_transacao_ui,    "atualizar"),
        ("Apagar",    apagar_transacao_ui,    "remover"),
        ("Limpar",    limpar_transacoes,      "limpar"),
    ]:
        btn(frm_btn, txt, cmd, tipo).pack(side=tk.LEFT, padx=5)

    lbl_msg_trans = tk.Label(tab, text="", font=F_SMALL, bg=C_BG)
    lbl_msg_trans.pack()

    outer = tk.LabelFrame(tab, text="  Registos  ", font=F_TITULO,
                          bg=C_FRAME, fg=C_TEXTO, relief="solid", bd=1)
    outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))
    inner = tk.Frame(outer, bg=C_FRAME)
    inner.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tabela_transacoes = treeview(inner,
        ("ID", "Tipo", "Descrição", "Valor", "Categoria"),
        [130, 90, 220, 100, 150])
    tabela_transacoes.bind("<<TreeviewSelect>>", selecionar_transacao)


def adicionar_transacao_ui():
    tipo = cb_trans_tipo.get()
    descricao = e_trans_descricao.get().strip()
    valor = e_trans_valor.get().strip().replace(",", ".")
    categoria = cb_trans_cat.get()
    id_orc = e_trans_id_orc.get().strip().upper() or None
    data_pagamento = e_trans_data_pag.get().strip()
    metodo_pagamento = cb_trans_metodo_pag.get()

    if not tipo:
        return msg_inline(lbl_msg_trans, "Escolha o tipo.", C_WARN)
    if not descricao:
        return msg_inline(lbl_msg_trans, "400: Descrição obrigatória.", C_ERROR)
    if not categoria:
        return msg_inline(lbl_msg_trans, "Escolha a categoria.", C_WARN)
    if not data_pagamento:
        return msg_inline(lbl_msg_trans, "Indique a data do pagamento.", C_WARN)
    try:
        datetime.strptime(data_pagamento, "%Y-%m-%d")
    except ValueError:
        return msg_inline(lbl_msg_trans, "400: Data inválida. Use YYYY-MM-DD.", C_ERROR)
    if not metodo_pagamento:
        return msg_inline(lbl_msg_trans, "Escolha o método de pagamento.", C_WARN)

    try:
        fval = float(valor)
        if fval <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_trans, "400: Valor inválido. Use: 12.50 ou 100.", C_ERROR)

    code, obj = adicionar_transacao(
        tipo, descricao, fval, categoria, conta_atual["id"], id_orc,
    )
    if code != 201:
        return msg_inline(lbl_msg_trans, f"{code}: {obj}", C_ERROR)

    code_p, obj_p = criar_pagamento(
        descricao=descricao,
        valor=fval,
        data=data_pagamento,
        metodo=metodo_pagamento,
        id_transacao=obj["id"],
    )

    if code_p != 201:
        # Evita ficar com uma transação sem pagamento associado.
        apagar_transacao(obj["id"])
        carregar_tabela_transacoes()
        atualizar_saldo()
        return msg_inline(
            lbl_msg_trans,
            f"Pagamento falhou: {code_p}: {obj_p}. A transação foi anulada.",
            C_ERROR,
        )

    aviso_orcamento = ""
    cor_msg = C_SUCCESS
    if tipo == "despesa" and id_orc:
        code_o, msg_o = registar_gasto(id_orc, fval)
        aviso_orcamento = f" | {msg_o}"
        if code_o != 200 or "AVISO" in str(msg_o):
            cor_msg = C_WARN

    msg_inline(
        lbl_msg_trans,
        f"✓ Transação {obj['id']} e pagamento {obj_p['id']} criados.{aviso_orcamento}",
        cor_msg,
    )
    set_status(f"Transação e pagamento criados → {obj['id']} / {obj_p['id']}")
    log.info("Transação adicionada → %s | Pagamento criado → %s", obj["id"], obj_p["id"])

    limpar_transacoes()
    carregar_tabela_transacoes()
    carregar_tabela_pagamentos()
    atualizar_saldo()


def consultar_transacao():
    uid = e_trans_id.get()
    if not uid:
        return msg_inline(lbl_msg_trans, "Selecione uma transação.", C_WARN)
    code, obj = encontrar_transacao(uid)
    if code == 200:
        msg_inline(lbl_msg_trans,
            f"{obj['id']}  |  {obj['tipo']}  |  {obj['descricao']}  |  "
            f"{obj['valor']:.2f}€  |  {obj['categoria']}", C_SUCCESS)
        set_status(f"Transação consultada → {uid}")
        log.info("Transação consultada → %s", uid)
    else:
        msg_inline(lbl_msg_trans, f"{code}: {obj}", C_ERROR)


def editar_transacao_ui():
    uid = e_trans_id.get()
    if not uid:
        return msg_inline(lbl_msg_trans, "Selecione uma transação.", C_WARN)
    valor_raw = e_trans_valor.get().strip().replace(",", ".")
    try:
        novo_val = float(valor_raw) if valor_raw else None
        if novo_val is not None and novo_val <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_trans, "400: Valor inválido.", C_ERROR)

    code, obj = editar_transacao(
        uid,
        descricao=e_trans_descricao.get() or None,
        valor=novo_val,
        categoria=cb_trans_cat.get() or None,
        id_orcamento=e_trans_id_orc.get().strip().upper() or None,
    )
    if code == 200:
        msg_inline(lbl_msg_trans, f"✓ Transação {uid} atualizada.", C_SUCCESS)
        set_status(f"Transação atualizada → {uid}")
        log.info("Transação atualizada → %s", uid)
        limpar_transacoes()
        carregar_tabela_transacoes()
        atualizar_saldo()
    else:
        msg_inline(lbl_msg_trans, f"{code}: {obj}", C_ERROR)


def apagar_transacao_ui():
    uid = e_trans_id.get()
    if not uid:
        return msg_inline(lbl_msg_trans, "Selecione uma transação.", C_WARN)
    if not messagebox.askyesno("Confirmação", f"Apagar transação {uid}?"):
        return
    code, obj = apagar_transacao(uid)
    if code == 200:
        msg_inline(lbl_msg_trans, f"✓ Transação {uid} apagada.", C_SUCCESS)
        set_status(f"Transação apagada → {uid}")
        log.info("Transação apagada → %s", uid)
        limpar_transacoes()
        carregar_tabela_transacoes()
        atualizar_saldo()
    else:
        msg_inline(lbl_msg_trans, f"{code}: {obj}", C_ERROR)


def carregar_tabela_transacoes():
    limpar_tree(tabela_transacoes)
    code, obj = listar_transacoes(id_conta=conta_atual.get("id"))
    if code == 200:
        for t in obj:
            linha(tabela_transacoes, (t["id"], t["tipo"], t["descricao"],
                                      f"{t['valor']:.2f}€", t["categoria"]))


def limpar_transacoes():
    limpar_widgets(e_trans_id, cb_trans_tipo, e_trans_descricao,
                   e_trans_valor, cb_trans_cat, e_trans_id_orc,
                   e_trans_data_pag, cb_trans_metodo_pag)
    set_entry(e_trans_data_pag, datetime.now().strftime("%Y-%m-%d"))


def selecionar_transacao(event):
    sel = tabela_transacoes.focus()
    if not sel:
        return
    v = tabela_transacoes.item(sel, "values")
    set_entry(e_trans_id, v[0], readonly=True)
    cb_trans_tipo.set(v[1])
    set_entry(e_trans_descricao, v[2])
    set_entry(e_trans_valor, v[3].replace("€", "").replace("+", "").replace("-", ""))
    cb_trans_cat.set(v[4])


# ══════════════════════════════════════════════════════════════
# TAB — ORÇAMENTOS
# ══════════════════════════════════════════════════════════════

def construir_tab_orcamentos():
    global e_orc_id, cb_orc_cat, e_orc_limite, cb_orc_period
    global tabela_orcamentos, lbl_msg_orc

    tab = tk.Frame(notebook, bg=C_BG)
    notebook.add(tab, text="  Orçamentos  ")

    frm = lf(tab, "Formulário — Orçamento")
    e_orc_id      = campo(frm, "ID",         0, col=0, readonly=True)
    cb_orc_cat    = combo(frm, "Categoria",  1, col=0, values=CATEGORIAS_ORCAMENTO)
    e_orc_limite  = campo(frm, "Limite (€)", 2, col=0)
    cb_orc_period = combo(frm, "Período",    3, col=0, values=PERIODOS)

    frm_btn = tk.Frame(tab, bg=C_BG)
    frm_btn.pack(pady=8)
    for txt, cmd, tipo in [
        ("Criar",     criar_orcamento_ui,     "criar"),
        ("Consultar", consultar_orcamento_ui, "consultar"),
        ("Atualizar", atualizar_orcamento_ui, "atualizar"),
        ("Remover",   remover_orcamento_ui,   "remover"),
        ("Limpar",    limpar_orcamentos,      "limpar"),
    ]:
        btn(frm_btn, txt, cmd, tipo).pack(side=tk.LEFT, padx=5)

    lbl_msg_orc = tk.Label(tab, text="", font=F_SMALL, bg=C_BG)
    lbl_msg_orc.pack()

    outer = tk.LabelFrame(tab, text="  Registos  ", font=F_TITULO,
                          bg=C_FRAME, fg=C_TEXTO, relief="solid", bd=1)
    outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))
    inner = tk.Frame(outer, bg=C_FRAME)
    inner.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tabela_orcamentos = treeview(inner,
        ("ID", "Categoria", "Limite", "Período", "Gasto Atual", "Restante"),
        [120, 160, 100, 100, 110, 110])
    tabela_orcamentos.bind("<<TreeviewSelect>>", selecionar_orcamento)


def criar_orcamento_ui():
    lim_raw = e_orc_limite.get().strip().replace(",", ".")
    try:
        fv = float(lim_raw)
        if fv <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_orc, "400: Limite inválido.", C_ERROR)
    code, obj = criar_orcamento(cb_orc_cat.get(), fv, cb_orc_period.get())
    if code == 201:
        msg_inline(lbl_msg_orc, f"✓ Orçamento {obj['id']} criado.", C_SUCCESS)
        set_status(f"Orçamento criado → {obj['id']}")
        log.info("Orçamento criado → %s", obj["id"])
        limpar_orcamentos()
        carregar_tabela_orcamentos()
    else:
        msg_inline(lbl_msg_orc, f"{code}: {obj}", C_ERROR)


def consultar_orcamento_ui():
    uid = e_orc_id.get()
    if not uid:
        return msg_inline(lbl_msg_orc, "Selecione um orçamento.", C_WARN)
    code, obj = consultar_orcamento(uid)
    if code == 200:
        rest = obj["limite"] - obj["gasto_atual"]
        msg_inline(lbl_msg_orc,
            f"{obj['id']}  |  {obj['categoria']}  |  limite {obj['limite']:.2f}€  |  "
            f"gasto {obj['gasto_atual']:.2f}€  |  restante {rest:.2f}€", C_SUCCESS)
        set_status(f"Orçamento consultado → {uid}")
        log.info("Orçamento consultado → %s", uid)
    else:
        msg_inline(lbl_msg_orc, f"{code}: {obj}", C_ERROR)


def atualizar_orcamento_ui():
    uid = e_orc_id.get()
    if not uid:
        return msg_inline(lbl_msg_orc, "Selecione um orçamento.", C_WARN)
    lim_raw = e_orc_limite.get().strip().replace(",", ".")
    try:
        novo_l = float(lim_raw) if lim_raw else None
        if novo_l is not None and novo_l <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_orc, "400: Limite inválido.", C_ERROR)
    code, obj = atualizar_orcamento(uid,
        limite=novo_l, categoria=cb_orc_cat.get() or None,
        periodo=cb_orc_period.get() or None)
    if code == 200:
        msg_inline(lbl_msg_orc, f"✓ Orçamento {uid} atualizado.", C_SUCCESS)
        set_status(f"Orçamento atualizado → {uid}")
        log.info("Orçamento atualizado → %s", uid)
        limpar_orcamentos()
        carregar_tabela_orcamentos()
    else:
        msg_inline(lbl_msg_orc, f"{code}: {obj}", C_ERROR)


def remover_orcamento_ui():
    uid = e_orc_id.get()
    if not uid:
        return msg_inline(lbl_msg_orc, "Selecione um orçamento.", C_WARN)
    if not messagebox.askyesno("Confirmação", f"Remover orçamento {uid}?"):
        return
    code, obj = remover_orcamento(uid)
    if code == 200:
        msg_inline(lbl_msg_orc, f"✓ Orçamento {uid} removido.", C_SUCCESS)
        set_status(f"Orçamento removido → {uid}")
        log.info("Orçamento removido → %s", uid)
        limpar_orcamentos()
        carregar_tabela_orcamentos()
    else:
        msg_inline(lbl_msg_orc, f"{code}: {obj}", C_ERROR)


def carregar_tabela_orcamentos():
    limpar_tree(tabela_orcamentos)
    code, obj = listar_orcamentos()
    if code == 200:
        for oid, d in obj.items():
            rest     = d["limite"] - d["gasto_atual"]
            excedido = rest < 0
            tag_extra = "excedido" if excedido else None
            linha(tabela_orcamentos, (oid, d["categoria"], f"{d['limite']:.2f}€",
                                      d["periodo"], f"{d['gasto_atual']:.2f}€",
                                      f"{rest:.2f}€"), tag_extra)


def limpar_orcamentos():
    limpar_widgets(e_orc_id, cb_orc_cat, e_orc_limite, cb_orc_period)


def selecionar_orcamento(event):
    sel = tabela_orcamentos.focus()
    if not sel:
        return
    v = tabela_orcamentos.item(sel, "values")
    set_entry(e_orc_id, v[0], readonly=True)
    cb_orc_cat.set(v[1])
    set_entry(e_orc_limite, v[2].replace("€", ""))
    cb_orc_period.set(v[3])


# ══════════════════════════════════════════════════════════════
# TAB — PAGAMENTOS
# ══════════════════════════════════════════════════════════════

def construir_tab_pagamentos():
    global e_pag_id, e_pag_descricao, e_pag_valor, e_pag_data
    global cb_pag_metodo, e_pag_id_trans
    global tabela_pagamentos, lbl_msg_pag

    tab = tk.Frame(notebook, bg=C_BG)
    notebook.add(tab, text="  Pagamentos  ")

    frm = lf(tab, "Formulário — Pagamento")
    e_pag_id        = campo(frm, "ID",                0, col=0, readonly=True)
    e_pag_descricao = campo(frm, "Descrição",         1, col=0)
    e_pag_valor     = campo(frm, "Valor (€)",         2, col=0)
    e_pag_data      = campo(frm, "Data (YYYY-MM-DD)", 3, col=0)
    cb_pag_metodo   = combo(frm, "Método",            0, col=1, values=METODOS_PAG)
    e_pag_id_trans  = campo(frm, "ID Transação",      1, col=1)
    set_entry(e_pag_data, datetime.now().strftime("%Y-%m-%d"))

    frm_btn = tk.Frame(tab, bg=C_BG)
    frm_btn.pack(pady=8)
    for txt, cmd, tipo in [
        ("Criar",     criar_pagamento_ui,     "criar"),
        ("Consultar", consultar_pagamento_ui, "consultar"),
        ("Atualizar", atualizar_pagamento_ui, "atualizar"),
        ("Remover",   remover_pagamento_ui,   "remover"),
        ("Limpar",    limpar_pagamentos,      "limpar"),
    ]:
        btn(frm_btn, txt, cmd, tipo).pack(side=tk.LEFT, padx=5)

    lbl_msg_pag = tk.Label(tab, text="", font=F_SMALL, bg=C_BG)
    lbl_msg_pag.pack()

    outer = tk.LabelFrame(tab, text="  Registos  ", font=F_TITULO,
                          bg=C_FRAME, fg=C_TEXTO, relief="solid", bd=1)
    outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 14))
    inner = tk.Frame(outer, bg=C_FRAME)
    inner.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    tabela_pagamentos = treeview(inner,
        ("ID", "Descrição", "Valor", "Data", "Método", "ID Transação"),
        [120, 200, 90, 110, 120, 130])
    tabela_pagamentos.bind("<<TreeviewSelect>>", selecionar_pagamento)


def criar_pagamento_ui():
    valor_raw = e_pag_valor.get().strip().replace(",", ".")
    try:
        fv = float(valor_raw)
        if fv <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_pag, "400: Valor inválido.", C_ERROR)
    code, obj = criar_pagamento(e_pag_descricao.get(), fv,
                                e_pag_data.get(), cb_pag_metodo.get(),
                                e_pag_id_trans.get() or None)
    if code == 201:
        msg_inline(lbl_msg_pag, f"✓ Pagamento {obj['id']} criado.", C_SUCCESS)
        set_status(f"Pagamento criado → {obj['id']}")
        log.info("Pagamento criado → %s", obj["id"])
        limpar_pagamentos()
        carregar_tabela_pagamentos()
    else:
        msg_inline(lbl_msg_pag, f"{code}: {obj}", C_ERROR)


def consultar_pagamento_ui():
    uid = e_pag_id.get()
    if not uid:
        return msg_inline(lbl_msg_pag, "Selecione um pagamento.", C_WARN)
    code, obj = consultar_pagamento(uid)
    if code == 200:
        msg_inline(lbl_msg_pag,
            f"{obj['id']}  |  {obj['descricao']}  |  {obj['valor']:.2f}€  |  "
            f"{obj['data']}  |  {obj['metodo']}", C_SUCCESS)
        set_status(f"Pagamento consultado → {uid}")
        log.info("Pagamento consultado → %s", uid)
    else:
        msg_inline(lbl_msg_pag, f"{code}: {obj}", C_ERROR)


def atualizar_pagamento_ui():
    uid = e_pag_id.get()
    if not uid:
        return msg_inline(lbl_msg_pag, "Selecione um pagamento.", C_WARN)
    valor_raw = e_pag_valor.get().strip().replace(",", ".")
    try:
        novo_v = float(valor_raw) if valor_raw else None
        if novo_v is not None and novo_v <= 0:
            raise ValueError
    except ValueError:
        return msg_inline(lbl_msg_pag, "400: Valor inválido.", C_ERROR)
    code, obj = atualizar_pagamento(uid,
        descricao=e_pag_descricao.get() or None,
        valor=novo_v,
        data=e_pag_data.get() or None,
        metodo=cb_pag_metodo.get() or None,
        id_transacao=e_pag_id_trans.get() or None)
    if code == 200:
        msg_inline(lbl_msg_pag, f"✓ Pagamento {uid} atualizado.", C_SUCCESS)
        set_status(f"Pagamento atualizado → {uid}")
        log.info("Pagamento atualizado → %s", uid)
        limpar_pagamentos()
        carregar_tabela_pagamentos()
    else:
        msg_inline(lbl_msg_pag, f"{code}: {obj}", C_ERROR)


def remover_pagamento_ui():
    uid = e_pag_id.get()
    if not uid:
        return msg_inline(lbl_msg_pag, "Selecione um pagamento.", C_WARN)
    if not messagebox.askyesno("Confirmação", f"Remover pagamento {uid}?"):
        return
    code, obj = remover_pagamento(uid)
    if code == 200:
        msg_inline(lbl_msg_pag, f"✓ Pagamento {uid} removido.", C_SUCCESS)
        set_status(f"Pagamento removido → {uid}")
        log.info("Pagamento removido → %s", uid)
        limpar_pagamentos()
        carregar_tabela_pagamentos()
    else:
        msg_inline(lbl_msg_pag, f"{code}: {obj}", C_ERROR)


def carregar_tabela_pagamentos():
    limpar_tree(tabela_pagamentos)
    code, obj = listar_pagamentos()
    if code == 200:
        for pid, d in obj.items():
            linha(tabela_pagamentos, (pid, d["descricao"], f"{d['valor']:.2f}€",
                                      d["data"], d["metodo"], d["id_transacao"] or "—"))


def limpar_pagamentos():
    limpar_widgets(e_pag_id, e_pag_descricao, e_pag_valor,
                   e_pag_data, cb_pag_metodo, e_pag_id_trans)
    set_entry(e_pag_data, datetime.now().strftime("%Y-%m-%d"))


def selecionar_pagamento(event):
    sel = tabela_pagamentos.focus()
    if not sel:
        return
    v = tabela_pagamentos.item(sel, "values")
    set_entry(e_pag_id, v[0], readonly=True)
    set_entry(e_pag_descricao, v[1])
    set_entry(e_pag_valor, v[2].replace("€", ""))
    set_entry(e_pag_data, v[3])
    cb_pag_metodo.set(v[4])
    set_entry(e_pag_id_trans, "" if v[5] == "—" else v[5])


# ══════════════════════════════════════════════════════════════
# JANELA PRINCIPAL
# ══════════════════════════════════════════════════════════════

janela = tk.Tk()
janela.title("Gestão Financeira")
janela.geometry("1100x720")
janela.minsize(900, 600)
janela.configure(bg=C_DARK)

aplicar_estilos()

# construir ambos os frames (login e app)
construir_login()
construir_app()

# arrancar no login
frame_atual = None
mostrar_frame(frame_login)

log.info("APP iniciada")
janela.mainloop()
