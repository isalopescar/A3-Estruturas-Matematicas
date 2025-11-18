# Bibliotecas

import numpy as np

# Dicionário de mensagens de erro

MSG = { 
    "erro_int": "Erro: Digite um número inteiro.",
    "erro_float": "Erro: Entrada inválida. Digite um número, ex: 10 ou 10.5.",
    "erro_intervalo": "Erro: Digite um número dentro do intervalo permitido.",
    "erro_negativo": "Erro: O valor não pode ser negativo.",
    "erro_opcao": "Erro: Opção inválida."
}

# Funções

def ler_int(msg): # leitura de int
    while True:
        entrada = input(msg)
        try:
            return int(entrada)
        except ValueError:
            print(MSG["erro_int"])

def ler_int_pos(msg): # leitura de int positivo
    while True:
        valor = ler_int(msg)  # recicla função ler_int
        if valor > 0:
            return valor
        else:
            print(MSG["erro_negativo"])

def ler_float(msg): # leitura de float
    while True:
        entrada = input(msg)
        try:
            return float(entrada)
        except ValueError:
            print(MSG["erro_float"])

def ler_float_pos(msg): # leitura de float positivo
    while True:
        valor = ler_float(msg) # recicla função ler_float
        if valor > 0:
            return valor
        print(MSG["erro_negativo"])

def ler_num_intervalo(func_ler, msg, min, max): # leitura de limite de intervalo
    while True:
        valor = func_ler(msg) # usa função de leitura desejada, ex: ler_int, ler_float, etc
        if min <= valor <= max:
            return valor
        print(MSG["erro_intervalo"])

def ler_opc_menu(msg, opcoes_validas): # leitura do menu de opções de restrição
    while True:
        entrada = input(msg)
        if entrada in opcoes_validas:
            return entrada
        print(MSG["erro_opcao"])

def ler_nome_cat(i): # leitura dos nomes das categorias definidas pelo usuário
    entrada = input(f"Categoria {i} (deixe em branco para usar nome padrão): ")
    return entrada if entrada else f"Categoria {i}"

def menu_cat(nomes): # menu de categorias definidas pelo usuário
    while True:
        print("\nEscolha a categoria:")
        for i, nome in enumerate(nomes,start=1):
            print(f"{i} - {nome}")
        opc = ler_num_intervalo(ler_int, "Número da categoria: ", 1, len(nomes))
        return opc - 1
    
def res_matriz(n, nomes, A, b): # validação e resolução da matriz inversa
    len_A = len(A)
    if len_A != n:
        print(f"\nErro: Número de restrições deve ser igual ao de categorias ({n}).")
        return None
    A_np = np.array(A)
    b_np = np.array(b)
    det_A = np.linalg.det(A_np)
    limite = 0.000000001
    if abs(det_A) < limite:
        print(f"\nErro: Restrições escohlidas não conseguem determinar um único orçamento. Tente modificar ou remover a última restrição para continuar.")
        return None
    A_inversa = np.linalg.inv(A_np)
    x_solucao = np.dot(A_inversa, b_np)
    return x_solucao, A_inversa, A_np, b_np

def exibir_res(nomes, x_solucao): # visualização do resultado final
    total = 0.0
    for i in range(len(nomes)):
        valor = x_solucao[i]
        print(f"{nomes[i]}: R$ {valor:.2f}")
        total += valor
    print(f"Orçamento total: R$ {total:.2f}")
    
# Ponto de entrada da interface

n = ler_num_intervalo(ler_int_pos, "Digite o número de categorias (1 a 4): ", 1, 4)
nomes = [ler_nome_cat(i+1) for i in range(n)]

# Construção das matrizes
while True:
    A = []
    b = []

    # Menu de opções de restrição

    while True:
        opc = ler_opc_menu("\nEscolha o(s) tipo(s) de restrição: \n1 - Valor total \n2 - Valor fixo para uma categoria \n3 - Razão entre duas categorias \n4 - Percentual do total \n0 - Terminar e resolver \nOpção: ", ["0","1","2","3","4"])
        if opc == "0":
            break

    # Opções de restrição

        if opc == "1": # Opção 1 - Valor total
            print("\nVocê escolheu: Valor total.")
            total = ler_float_pos("Digite o valor total do orçamento: ")
            linha = [1.0] * n 
            A.append(linha)
            b.append(total)
            print(f"Restrição de valor total adicionada: R$ {total:.2f}")

        elif opc == "2": # Opção 2 - Valor fixo para uma categoria
            print("\nVocê escolheu: Valor fixo para uma categoria.")
            idx = menu_cat(nomes)
            valor = ler_float_pos(f"Digite o valor que '{nomes[idx]}' deve receber: ")
            linha = [0.0] * n
            linha[idx] = 1.0
            A.append(linha)
            b.append(valor)
            print(f"Restrição a categoria adicionada: {nomes[idx]} = R$ {valor:.2f}")

        elif opc == "3": # Opção 3 - Razão entre duas categorias
            print("\nVocê escolheu: Razão entre duas categorias.")
            idxA = menu_cat(nomes)
            idxB = menu_cat(nomes)
            if idxA == idxB:
                print("Erro: As duas categorias devem ser diferentes.")
                continue
            fator = ler_float(f"Digite o fator para '{nomes[idxA]}' = fator * '{nomes[idxB]}' (ex: 2 para dobro): ")
            linha = [0.0] * n
            linha[idxA] = 1.0
            linha[idxB] = -fator
            A.append(linha)
            b.append(0.0)
            print(f"Restrição de razão adicionada: {nomes[idxA]} = {fator} * {nomes[idxB]}")

        elif opc == '4': # Opção 4 - Percentual do total
            print("\nVocê escolheu: Percentual do total.")
            idx = menu_cat(nomes)
            pct = ler_num_intervalo(ler_float, f"Digite o percentual para {nomes[idx]} (0 a 100): ", 0, 100)
            fator = pct / 100.0
            linha = [0.0] * n
            linha[idx] = 1.0
            A.append(linha)
            b.append(fator)
            print(f"Restrição de percentual adicionada: {nomes[idx]} = {pct}% do total")
    # Resolução final da matriz

    result = res_matriz(n, nomes, A, b)
    if result is not None:
        x_solucao, A_inversa, A_np, b_np = result
        exibir_res(nomes, x_solucao)
        break