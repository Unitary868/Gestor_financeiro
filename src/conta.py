# conta.py – Entidade Conta
import random, string
from utils import pedir_num, pedir_texto, sep, cab, pausar

# ── Dados globais ─────────────────────────────────────────────
conta = {}

# ── Helpers internos ──────────────────────────────────────────
def gerar_id():
    return random.randint(1000, 9999)

def gerar_token(uid):
    l = "".join(random.choices(string.ascii_uppercase, k=3))
    n = "".join(random.choices(string.digits, k=3))
    return f"USR-{uid}-{l}{n}"

def pedir_pin():
    while True:
        p = input("  PIN (4 dígitos): ").strip()
        if p.isdigit() and len(p) == 4:
            return p
        print("  400 - Bad Request: PIN inválido, deve ter 4 dígitos.")

# ── CRUD ──────────────────────────────────────────────────────
def criar_conta(nome, nif, pin):
    try:
        if conta:
            return (409, "Já existe uma conta criada.")
        uid   = gerar_id()
        token = gerar_token(uid)
        conta["id"]    = uid
        conta["nome"]  = nome
        conta["nif"]   = nif
        conta["pin"]   = pin
        conta["token"] = token
        return (201, f"Conta criada com sucesso.\n  ID:    {uid}\n  Token: {token}")
    except Exception as e:
        return (500, str(e))

def conta_existe():
    try:
        return (200, bool(conta))
    except Exception as e:
        return (500, str(e))

def verificar_login(uid, pin):
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        if conta.get("id") == uid and conta.get("pin") == pin:
            return (200, "Login bem-sucedido.")
        return (401, "ID ou PIN incorretos.")
    except Exception as e:
        return (500, str(e))

def atualizar_pin(uid, pin_atual, pin_novo):
    try:
        status, msg = verificar_login(uid, pin_atual)
        if status != 200:
            return (status, msg)
        conta["pin"] = pin_novo
        return (200, "PIN atualizado com sucesso.")
    except Exception as e:
        return (500, str(e))

def eliminar_conta(uid, pin):
    try:
        status, msg = verificar_login(uid, pin)
        if status != 200:
            return (status, msg)
        conta.clear()
        return (200, "Conta eliminada com sucesso.")
    except Exception as e:
        return (500, str(e))

def get_dados():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, {
            "id":    conta.get("id",    "—"),
            "nome":  conta.get("nome",  "—"),
            "nif":   conta.get("nif",   "—"),
            "token": conta.get("token", "—"),
        })
    except Exception as e:
        return (500, str(e))

def get_nome():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("nome", "—"))
    except Exception as e:
        return (500, str(e))

def get_id():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("id", "—"))
    except Exception as e:
        return (500, str(e))

def get_token():
    try:
        if not conta:
            return (404, "Nenhuma conta encontrada.")
        return (200, conta.get("token", "—"))
    except Exception as e:
        return (500, str(e))

# ── Menu Conta ────────────────────────────────────────────────
def menu_conta():
    while True:
        cab("👤 CONTA")
        id_rc   = get_id()
        dados_rc = get_dados()
        uid = id_rc[1] if id_rc[0] == 200 else None

        if dados_rc[0] == 200:
            d = dados_rc[1]
            sep()
            print(f"  👤 Nome:  {d['nome']}")
            print(f"  🆔 ID:    {d['id']}")
            print(f"  📋 NIF:   {d['nif']}")
            print(f"  🔑 Token: {d['token']}")
            sep()

        print("  1-Atualizar PIN   2-Eliminar Conta   0-Voltar")
        sep()
        o = input("\n  Opção: ").strip()

        if o == "0":
            break

        elif o == "1":
            cab("🔑 ATUALIZAR PIN")
            pin_atual = pedir_pin()
            pin_novo  = pedir_pin()
            rc = atualizar_pin(uid, pin_atual, pin_novo)
            print(f"  {rc[0]} - {rc[1]}")
            pausar()

        elif o == "2":
            cab("🗑️ ELIMINAR CONTA")
            pin = pedir_pin()
            if input("  Tens a certeza? Todos os dados serão apagados (s/n): ").strip().lower() != "s":
                print("  ❌ Cancelado.")
                pausar()
                continue
            rc = eliminar_conta(uid, pin)
            print(f"  {rc[0]} - {rc[1]}")
            pausar()
            if rc[0] == 200:
                return True   # sinaliza ao main que a conta foi eliminada

        else:
            print("  400 - Bad Request: Opção inválida.")

    return False
