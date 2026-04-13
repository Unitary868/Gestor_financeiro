# utils.py – Funções auxiliares, validação, ID e token

import os, random, string

def limpar():
    os.system("cls" if os.name == "nt" else "clear")
def sep():
    print("─" * 60)
def cab(t):
    print("\n" + "═"*60 + f"\n  {t}\n" + "═"*60)
def pausar():
    input("\n  Pressione Enter para continuar...")

# ── Números ───────────────────────────────────────────────────

def pedir_num(msg, mn=None, mx=None, dec=True):
    while True:
        try:
            v = (float if dec else int)(input(msg).strip().replace(",", "."))
            if (mn is None or v >= mn) and (mx is None or v <= mx):
                return v
            print(f"  400 - Bad Request: Valor fora do intervalo {mn} – {mx}.")
        except ValueError:
            print("  400 - Bad Request: Número inválido.")

# ── Texto ─────────────────────────────────────────────────────

def pedir_texto(msg):
    while True:
        t = input(msg).strip()
        if t:
            return t
        print("  400 - Bad Request: Campo obrigatório.")

# ── Validação de campos ───────────────────────────────────────

def pedir_nif():
    while True:
        n = input("  NIF (9 dígitos): ").strip()
        if n.isdigit() and len(n) == 9:
            return n
        print("  400 - Bad Request: NIF inválido, deve ter 9 dígitos.")

def pedir_pin():
    while True:
        p = input("  PIN (4 dígitos): ").strip()
        if p.isdigit() and len(p) == 4:
            return p
        print("  400 - Bad Request: PIN inválido, deve ter 4 dígitos.")

def pedir_password():
    while True:
        p = input("  Password (mín. 6 caracteres): ")
        if len(p) < 6:
            print("  400 - Bad Request: Password demasiado curta.");
            continue
        c = input("  Confirmar password: ")
        if p == c:
            return p
        print("  400 - Bad Request: Passwords não coincidem.")

# ── ID e Token ────────────────────────────────────────────────

def gerar_id():
    return random.randint(1000, 9999)

def gerar_token(uid):
    l = "".join(random.choices(string.ascii_uppercase, k=3))
    n = "".join(random.choices(string.digits, k=3))
    return f"USR-{uid}-{l}{n}"
