## RELATÓRIO FINAL DO PROJETO A3 - ORÇAMENTO POR INVERSÃO DE MATRIZES

**Unidade Curricular:** Estruturas Matemáticas  
**Tema:** Inversão de Matrizes

**(Importante) Integrantes / RA / CONTRIBUIÇÕES:**
- Isadora Lopes Carneiro — 12724112679 / fez o script, corrigiu partes de Luiggi e Raimundo, montou slide
- João Luiz — 12724114136 / apresentou slide no dia
- Arthur Ornelas — 12724128058 / não participou
- Alisson Conceição — 12724216237 / apresentou slide no dia
- Luiggi Souza Grassi — 12724143600 / implementou sistema de logs
- Raimundo Neto — 12724119913 / fez relatório README

**Repositório GitHub:** <https://github.com/isalopescar/A3-Estruturas-Matematicas>

**Bibliotecas necessárias:**
- `numpy`
- `os`
- `datetime`

---

### 1. Introdução

Este projeto consiste na criação de um programa em Python (`budget.py`) que utiliza o conceito deInversão de Matrizes para criar um orçamento doméstico automático. O objetivo é distribuir um valor total entre diversas categorias (variáveis) com base em um conjunto de regras (equações lineares) definidas pelo usuário.

---

### 2. Fundamentação Teórica

O problema de distribuir o orçamento entre $n$ categorias com $n$ restrições lineares é traduzido em um Sistema de Equações Lineares, representado na forma matricial:

$$\mathbf{A} \cdot \mathbf{x} = \mathbf{b}$$

Onde:
- $\mathbf{x}$ é o vetor das incógnitas (os valores a serem alocados a cada categoria).
- $\mathbf{A}$ é a Matriz de Coeficientes ($n \times n$), construída a partir das restrições do usuário.
- $\mathbf{b}$ é o vetor dos Termos Independentes (os valores numéricos das restrições).

#### A Solução por Inversão

Para que o sistema tenha uma solução única, a matriz $\mathbf{A}$ deve ser quadrada e inversível (ou seja, seu determinante deve ser diferente de zero, $det(\mathbf{A}) \ne 0$).

Nesse caso, a solução é encontrada usando a matriz inversa $\mathbf{A}^{-1}$:

$$\mathbf{x} = \mathbf{A}^{-1} \cdot \mathbf{b}$$

O script `budget.py` utiliza as funções do `numpy` (`linalg.inv` e `linalg.det`) para executar este cálculo, sendo este o núcleo matemático da solução.

---

### 3. Descrição Funcional do Programa

O programa orienta o usuário a definir as categorias e, em seguida, fornecer exatamente o mesmo número de restrições para garantir uma matriz $\mathbf{A}$ quadrada.

#### 3.1. Tipos de Restrições

O usuário pode escolher entre quatro tipos de restrições, cada um traduzido em uma linha da matriz $\mathbf{A}$ e do vetor $\mathbf{b}$:

| Opção | Restrição Definida pelo Usuário | Forma da Equação no Sistema                                 |
| :---: | :------------------------------ | :---------------------------------------------------------- |
|   1   | Valor Total                     | Soma de todas as categorias é igual a $T$.                  |
|   2   | Valor Fixo                      | Uma categoria específica recebe um valor $V$.               |
|   3   | Razão                           | Uma categoria $i$ é um múltiplo $r$ de outra categoria $j$. |
|   4   | Percentual                      | Uma categoria $i$ equivale a $p\%$ do valor Total.          |

#### 3.2. Rastreamento e Validação (Log)

O script incorpora um sistema de log (`gerar_log`) que registra todos os passos da resolução em arquivos na pasta `/logs`. Isso inclui:
- Os dados de entrada (restrições, $\mathbf{A}$, $\mathbf{b}$).
- Os passos matemáticos (determinante, $\mathbf{A}^{-1}$, e solução $\mathbf{x}$).
- O resultado final ou a mensagem de erro.

A função principal (`res_matriz`) realiza validações cruciais:
- **Não Singularidade:** Verifica se $det(\mathbf{A})$ é zero. Se for, informa que as restrições são redundantes ou conflitantes (matriz singular), impedindo uma solução única.
- **Valores Positivos:** Impede que a solução matemática gere valores negativos para o orçamento, o que não faz sentido no contexto financeiro.

---

### 4. Exemplo de Aplicação e Resultados

O projeto foi validado com diversos testes. Abaixo está um exemplo que demonstra a resolução de um sistema $3 \times 3$:

**Cenário:** Orçamento de R$ 1500 com 3 categorias: Alimentação ($x_1$), Transporte ($x_2$), Lazer ($x_3$).

**Restrições Fornecidas:**
1.  Alimentação = R$ 500 (Valor Fixo)
2.  Alimentação = 2 × Transporte (Razão)
3.  $x_1 + x_2 + x_3 = 1500$ (Valor Total)

**Matriz A e Vetor b:**  

$$\mathbf{A} = \begin{pmatrix} 1 & 0 & 0 \\ 1 & -2 & 0 \\ 1 & 1 & 1 \end{pmatrix}, \quad \mathbf{b} = \begin{pmatrix} 500 \\ 0 \\ 1500 \end{pmatrix}$$

**Solução por $\mathbf{x} = \mathbf{A}^{-1} \cdot \mathbf{b}$:**

1.  **Determinante de $\mathbf{A}$:** $det(\mathbf{A}) = -2$ (matriz inversível).
2.  **Solução Calculada (Passos no Log):**  

    $$\mathbf{x} = \begin{pmatrix} 500 \\ 250 \\ 750 \end{pmatrix}$$

**Orçamento Final:**
- Alimentação: R$ 500,00
- Transporte: R$ 250,00
- Lazer: R$ 750,00
- **Total:** R$ 1500,00

---

### 5. Conclusão

O projeto cumpriu o requisito de aplicar a **Inversão de Matrizes** na solução de um problema real. O script `budget.py` consegue transformar um conjunto de regras (restrições) em um orçamento final coerente e único, desde que as regras não sejam contraditórias ou redundantes (matriz não singular). O sistema de log implementado garante a transparência do processo, registrando todos os cálculos matriciais para fins de auditoria e validação.
