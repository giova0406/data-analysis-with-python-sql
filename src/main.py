# EXERCÍCIO 1 - LISTAR OS IDIOMAS ORIGINAIS DOS FILMES

import sqlite3 # Importacao da biblioteca para trabalhar com banco de dados sqlite3

conn = sqlite3.connect('cinema (1).sqlite')
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT idioma_original FROM filmes")
Resultado = cursor.fetchall()

for idioma in Resultado:
    print(idioma)

# EXERCÍCIO 2 - LISTAR OS ESTÚDIOS DOS FILMES

cursor.execute("SELECT DISTINCT estudio FROM filmes")
Resultado2 = cursor.fetchall() # Recupera os estúdios distintos dos filmes
for estudio in Resultado2:
    print(estudio)


# EXERCÍCIO 3 - CALCULAR A MÉDIA DE RECEITA POR ESTÚDIO

cursor.execute("SELECT estudio, receita_milhoes FROM filmes ")
dados = cursor.fetchall() # Recupera os dados de estúdio e receita em milhões para todos os filmes

grupos = {} # dicionário para armazenar as receitas agrupadas por estúdio
for estudio, receita_milhoes in dados:
    if estudio not in grupos: # se o estúdio ainda não estiver no dicionário, inicializa uma lista para ele
        grupos[estudio] = [] # adiciona a receita do filme à lista do estúdio correspondente
    grupos[estudio].append(receita_milhoes) 

for estudio, receitas in grupos.items():
    if receitas: #evita divisão por zero
        media = sum(receitas) / len(receitas) # calcula a média de receita para o estúdio
        print(f"{estudio}: {media:.2f} milhões") # formata a média para exibir com duas casas decimais
  
# 5 - LISTAR OS DIRETORES COM MAIS DE 4 FILMES
cursor.execute("SELECT diretor,titulo_original FROM filmes ")
dados = cursor.fetchall()

contagem_diretores = {} # dicionário para contar o número de filmes por diretor

for diretor,titulo_original in dados:
    if diretor not in contagem_diretores:
        contagem_diretores[diretor] = 0
    contagem_diretores[diretor] += 1

for diretor, qnt in contagem_diretores.items():
    if qnt >= 4:
        print(f'O {diretor} Tem {qnt} de Filmes')

# 6 - LISTAR OS FILMES COM RECEITA MAIOR QUE 100 MILHÕES
cursor.execute("SELECT orcamento_milhoes, pais_origem FROM filmes")
dados = cursor.fetchall()  # pega os dados

g_milhoes = {}  # dicionário para agrupar
for orcamento_milhoes, pais_origem in dados:
    if pais_origem not in g_milhoes:
        g_milhoes[pais_origem] = []
    g_milhoes[pais_origem].append(orcamento_milhoes)

medias = []
for pais, valores in g_milhoes.items():
    media = sum(valores) / len(valores)
    if media > 100:
        medias.append((pais, media))

# ordenar fora do loop
medias.sort(key=lambda x: x[1], reverse=True)
for pais, media in medias:
    print(f'{pais}: {media:.2f} milhões')


# 7 - CALCULAR A QUANTIDADE, SOMA E MÉDIA DAS DURAÇÕES DOS FILMES POR ESTÚDIO

cursor.execute("SELECT duracao_minutos FROM filmes")
dados = cursor.fetchall()

duracoes = [
    [148, 125, 132, 118],
    [150, 98, 142],
    [128, 175, 138, 145, 112]
]

def quantidade_filmes(matriz):
    resultado = []
    for estudio in matriz:
        resultado.append(len(estudio))
    return resultado

def soma_duracoes(matriz):
    resultado = []
    for estudio in matriz:
        resultado.append(sum(estudio))
    return resultado

def media_duracoes(matriz):
    resultado = []
    for estudio in matriz:
        media = sum(estudio) / len(estudio)
        resultado.append(media)
    return resultado

print(quantidade_filmes(duracoes))
print(soma_duracoes(duracoes))
print(media_duracoes(duracoes))

# 11 - CALCULAR O TOTAL DE INDICAÇÕES POR PRÊMIO E POR ANO, E IDENTIFICAR O PRÊMIO E O ANO COM MAIS INDICAÇÕES

indicacoes = [
    [12, 8, 15, 10, 9],   # Oscar
    [8, 6, 10, 7, 5],     # Globo de Ouro
    [10, 9, 12, 8, 7],    # BAFTA
    [5, 4, 6, 3, 4]       # Cannes
]

premios = ["Oscar", "Globo de Ouro", "BAFTA", "Cannes"]
anos = [2020, 2021, 2022, 2023, 2024]

def total_por_premio(matriz):
    resultado = []
    for linha in matriz:
        resultado.append(sum(linha))
    return resultado

def total_por_ano(matriz):
    resultado = []
    for i in range(len(matriz[0])):
        soma = 0
        for linha in matriz:
            soma += linha[i]
        resultado.append(soma)
    return resultado

def premio_com_mais(matriz, premios):
    totais = total_por_premio(matriz)
    max_valor = max(totais)
    indice = totais.index(max_valor)
    return premios[indice], max_valor

def ano_com_mais(matriz, anos):
    totais = total_por_ano(matriz)
    max_valor = max(totais)
    indice = totais.index(max_valor)
    return anos[indice], max_valor

print(total_por_premio(indicacoes))
print(total_por_ano(indicacoes))
print(premio_com_mais(indicacoes, premios))
print(ano_com_mais(indicacoes, anos))

# 15 - CALCULAR O CRESCIMENTO PERCENTUAL, TENDÊNCIA DE ALTA, GÊNERO MAIS VOLÁTIL E PARTICIPAÇÃO DE MERCADO DOS GÊNEROS DE FILMES

cursor.execute("""
SELECT generos.nome, filmes.receita_milhoes
FROM filmes
JOIN filme_genero ON filmes.id = filme_genero.filme_id
JOIN generos ON filme_genero.genero_id = generos.id
""")
dados = cursor.fetchall()

bilheteria = [
    [450, 520, 480, 610, 720],  # Ação
    [280, 310, 295, 340, 380],  # Comédia
    [180, 165, 190, 210, 250],  # Drama
    [120, 95, 130, 85, 110],    # Terror
    [350, 420, 390, 480, 550]   # Ficção Científica
]

generos = ["Ação", "Comédia", "Drama", "Terror", "Ficção Científica"]
anos = [2020, 2021, 2022, 2023, 2024]

def crescimento_percentual(matriz):
    resultado = []
    for linha in matriz:
        crescimento = ((linha[-1] - linha[0]) / linha[0]) * 100
        resultado.append(crescimento)
    return resultado

def tendencia_alta(matriz, generos):
    resultado = []
    for i, linha in enumerate(matriz):
        for j in range(len(linha) - 2):
            if linha[j] < linha[j+1] < linha[j+2]:
                resultado.append(generos[i])
                break
    return resultado

def genero_mais_volatil(matriz, generos):
    max_diff = 0
    genero_volatil = ""
    for i, linha in enumerate(matriz):
        diff = max(linha) - min(linha)
        if diff > max_diff:
            max_diff = diff
            genero_volatil = generos[i]
    return genero_volatil, max_diff

def participacao_mercado(matriz, generos):
    ultimo_ano = [linha[-1] for linha in matriz]
    total = sum(ultimo_ano)
    
    resultado = []
    for i, valor in enumerate(ultimo_ano):
        porcentagem = (valor / total) * 100
        resultado.append((generos[i], porcentagem))
    
    return resultado

print("Crescimento:", crescimento_percentual(bilheteria))
print("Tendência de alta:", tendencia_alta(bilheteria, generos))
print("Mais volátil:", genero_mais_volatil(bilheteria, generos))
print("Participação:", participacao_mercado(bilheteria, generos))
