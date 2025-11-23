import numpy as np
import os
from datetime import datetime

# ===================== LOG ===================== #

def gerar_log(operacao, dados, passos, resultado=None, erro=None):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/{operacao}_{timestamp}.log"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== LOG DO SISTEMA DE ORÇAMENTO ===\n")
        f.write(f"Operação: {operacao}\n")
        f.write(f"Timestamp: {timestamp}\n\n")

        f.write("=== Dados de Entrada ===\n")
        for k, v in dados.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

        f.write("=== Passos Matemáticos ===\n")
        for p in passos:
            f.write(f"- {p}\n")
        f.write("\n")

        if resultado is not None:
            f.write("=== Resultado ===\n")
            f.write(str(resultado) + "\n\n")

        if erro:
            f.write("=== ERRO ===\n")
            f.write(str(erro) + "\n")

    return filename


# ===================== MENSAGENS ===================== #

MSG = { 
    "erro_int": "Erro: Digite um número inteiro.",
    "erro_float": "Erro: Entrada inválida. Digite um número, ex: 10 ou 10.5.",
    "erro_intervalo": "Erro: Digite um número dentro do intervalo permitido.",
    "erro_negativo": "Erro: O valor não pode ser negativo.",
    "erro_opcao": "Erro: Opção inválida."
}


# ===================== FUNÇÕES DE LEITURA ===================== #

def ler_int(msg):
    while True:
        entrada = input(msg)
        try:
            return int(entrada)
        except ValueError:
            print(MSG["erro_int"])

def ler_int_pos(msg):
    while True:
        valor = ler_int(msg)
        if valor > 0:
            return valor
        print(MSG["erro_negativo"])

def ler_float(msg):
    while True:
        entrada = input(msg)
        try:
            return float(entrada)
        except ValueError:
            print(MSG["erro_float"])

def ler_float_pos(msg):
    while True:
        valor = ler_float(msg)
        if valor > 0:
            return valor
        print(MSG["erro_negativo"])

def ler_num_intervalo(func, msg, min, max):
    while True:
        valor = func(msg)
        if min <= valor <= max:
            return valor
        print(MSG["erro_intervalo"])

def ler_opc_menu(msg, opcoes):
    while True:
        entrada = input(msg)
        if entrada in opcoes:
            return entrada
        print(MSG["erro_opcao"])

def ler_nome_cat(i):
    entrada = input(f"Categoria {i} (deixe vazio para padrão): ")
    return entrada if entrada else f"Categoria {i}"

def menu_cat(nomes):
    while True:
        print("\nEscolha a categoria:")
        for i, nome in enumerate(nomes, start=1):
            print(f"{i} - {nome}")
        opc = ler_num_intervalo(ler_int, "Número da categoria: ", 1, len(nomes))
        return opc - 1


# ===================== RESOLUÇÃO DA MATRIZ ===================== #

def res_matriz(n, nomes, A, b):
    passos = []

    try:
        passos.append(f"Número de categorias: {n}")
        passos.append(f"Número de restrições: {len(A)}")

        if len(A) != n:
            erro = f"Número de restrições deve ser igual ao número de categorias ({n})."
            passos.append(erro)
            gerar_log("res_matriz", {"nomes": nomes, "A": A, "b": b}, passos, erro=erro)
            print("\nErro:", erro)
            return None

        A_np = np.array(A, dtype=float)
        b_np = np.array(b, dtype=float)

        passos.append(f"Matriz A:\n{A_np}")
        passos.append(f"Vetor b:\n{b_np}")

        det = np.linalg.det(A_np)
        passos.append(f"Determinante de A = {det}")

        if abs(det) < 1e-9:
            erro = "A matriz é singular (restrições inconsistentes ou redundantes)."
            passos.append(erro)
            gerar_log("res_matriz", {"nomes": nomes, "A": A, "b": b}, passos, erro=erro)
            print("\nErro:", erro)
            print("Restrições removidas. Recomece a adicionar.")
            return None

        passos.append("Calculando A⁻¹...")
        A_inv = np.linalg.inv(A_np)
        passos.append(f"Matriz inversa A⁻¹:\n{A_inv}")

        passos.append("Calculando x = A⁻¹ · b...")
        x = np.dot(A_inv, b_np)
        passos.append(f"Solução encontrada: {x}")

        if np.any(x < 0):
            erro = "A solução matemática contém valores negativos, inválidos para orçamento."
            passos.append(erro)
            dados_log = {"nomes": nomes, "A": A, "b": b}
            gerar_log("res_matriz", dados_log, passos, resultado=x, erro=erro)
            print(MSG["erro_negativo"])
            return None

        resultado_final = {nomes[i]: float(x[i]) for i in range(n)}

        gerar_log(
            "res_matriz",
            {"nomes": nomes, "A": A, "b": b},
            passos,
            resultado=resultado_final
        )

        return x, A_inv, A_np, b_np

    except Exception as e:
        passos.append(f"Erro inesperado: {e}")
        gerar_log("res_matriz", {"nomes": nomes, "A": A, "b": b}, passos, erro=e)
        print("\nErro inesperado na resolução.")
        return None


# ===================== RESULTADO ===================== #

def exibir_res(nomes, x):
    total = 0
    for i in range(len(nomes)):
        print(f"{nomes[i]}: R$ {x[i]:.2f}")
        total += x[i]
    print(f"Orçamento total: R$ {total:.2f}")

# ===================== FUNÇÃO AUXILIAR DE EXIBIÇÃO ===================== #

def formatar_retricao(opc, val_ou_cat, valor=None, fator=None):
    if opc == "1":
        return f"Total: R$ {val_ou_cat:.2f}"
    elif opc =="2":
        return f"Fixo: {val_ou_cat} = R$ {valor:.2f}"
    elif opc == "3":
        return f"Razão: {val_ou_cat[0]} = {fator} x {val_ou_cat[1]}"
    elif opc == "4":
        return f"Percentual: {val_ou_cat} = {valor}% do Total"
    return "Restrição inexistente"



# ===================== INTERFACE PRINCIPAL ===================== #

n = ler_num_intervalo(ler_int_pos, "Digite o número de categorias (1 a 4): ", 1, 4)
nomes = [ler_nome_cat(i+1) for i in range(n)]

while True:
    A = []
    b = []
    lista_restricoes = []
    
    while len(A) < n:
        resto = n - len(A)
        print(f"\nEscolha o tipo de restrição (restantes: {resto}):\n")
        opc = ler_opc_menu(
            "1 - Valor total\n"
            "2 - Valor fixo para uma categoria\n"
            "3 - Razão entre categorias\n"
            "4 - Percentual do total\n"
            "0 - Visualizar/remover restrições e resolver\n"
            "Opção: ",
            ["0", "1", "2", "3", "4"]
        )

        if opc == "0":
            if len(A) == n:
                break
            if len(A) == 0:
                print("\nNenhuma restrição aplicada ainda.")
                continue
            print("\nRestrições Atuais:")
            for i, r in enumerate(lista_restricoes, start=1):
                print(f"{i}: {r}")
            print("\n")
            opc_rev = ler_opc_menu("Deseja remover todas as retrições e recomeçar? (s/n): ", ["s", "S", "n", "N"])
            if opc_rev.lower() == "s":
                A.clear()
                b.clear()
                lista_restricoes.clear()
                print("Restrições removidas. Recomece a adicionar.")
            else:
                continue

        # ----------------- 1 - VALOR TOTAL ----------------- #
        elif opc == "1":
            print("\nVocê escolheu: Valor total")
            total = ler_float_pos("Digite o valor total: ")
            A.append([1.0] * n)
            b.append(total)
            lista_restricoes.append(formatar_retricao(opc, total))
            print(f"Restrição adicionada: Total = R$ {total:.2f}")

        # ----------------- 2 - VALOR FIXO ------------------ #
        elif opc == "2":
            print("\nVocê escolheu: Valor fixo para uma categoria")
            idx = menu_cat(nomes)
            valor = ler_float_pos(f"Valor para '{nomes[idx]}': ")
            linha = [0.0] * n
            linha[idx] = 1.0
            A.append(linha)
            b.append(valor)
            lista_restricoes.append(formatar_retricao(opc, nomes[idx], valor=valor))
            print(f"{nomes[idx]} = R$ {valor:.2f}")

        # ----------------- 3 - RAZÃO ENTRE CATEGORIAS ------- #
        elif opc == "3":
            print("\nVocê escolheu: Razão entre categorias")
            idxA = menu_cat(nomes)
            idxB = menu_cat(nomes)
            if idxA == idxB:
                print("Erro: as categorias devem ser diferentes.")
                continue
            fator = ler_float("Digite o fator (ex: 2 para dobro): ")
            linha = [0.0] * n
            linha[idxA] = 1.0
            linha[idxB] = -fator
            A.append(linha)
            b.append(0.0)
            lista_restricoes.append(formatar_retricao(opc, (nomes[idxA], nomes[idxB]), fator=fator))
            print(f"{nomes[idxA]} = {fator} × {nomes[idxB]}")

        # ----------------- 4 - PERCENTUAL DO TOTAL ---------- #
        elif opc == "4":
            print("\nVocê escolheu: Percentual do total")
            idx = menu_cat(nomes)
            pct = ler_num_intervalo(ler_float, f"Percentual (0 a 100) para {nomes[idx]}: ", 0, 100)
            fator = pct / 100.0
            linha = [-fator] * n
            linha[idx] = 1 - fator
            A.append(linha)
            b.append(0.0)
            lista_restricoes.append(formatar_retricao(opc, nomes[idx], valor=pct))
            print(f"{nomes[idx]} = {pct}% do total")

    if len(A) == n:
        print("\nRestrições Atingidas\n")

    # ===================== RESOLVER ===================== #
    result = res_matriz(n, nomes, A, b)

    if result is not None:
        x, _, _, _ = result
        exibir_res(nomes, x)
        break
    else:
        pass