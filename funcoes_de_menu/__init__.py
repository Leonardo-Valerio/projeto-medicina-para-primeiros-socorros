from funcoes_de_cadastro import *
import requests
import os
from dotenv import load_dotenv
import openai
import time
import dotenv
import tiktoken
load_dotenv()
api_key = os.getenv('MAPS_API_KEY')
def puxar_coordenadas(cep,api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        resposta = response.json()
        localizacao = resposta["results"][0]["geometry"]["location"]
        return localizacao

def encontrar_hospitais(latitude, longitude, api_key,area):
    max_area = 50000
    if area >= max_area:
        print('a area para busca excedeu os limites')
        return
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius={area}&type=hospital&key={api_key}"
    response = requests.get(places_url)
    if response.status_code == 200:
        dados = response.json()
        if len(dados["results"]) == 0:
            print(f'nenhum hospital achado na area de {area} metros')
            linha()
            area+=1000
            encontrar_hospitais(latitude,longitude,api_key,area)
        for i in dados["results"]:
            print(f'Hospital: {i["name"]} - Endereço: {i["vicinity"]}')
        linha()
        print(f'esses foram os hospitais encontrados em uma area de {area} metros')

def buscar_cep_usuario(nome):
    try:
        with open('./arquivo_cadastros/cadastros.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

    except FileNotFoundError:
        print("O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}.")
    else:
        dados_ordenados = quick_sort(dados, "nome")
        for usuario in dados_ordenados:
            print('----')
            print(usuario["nome"])
        resposta = binary_search(dados_ordenados,"nome","cep",nome)
        return resposta

def quick_sort(lista, chave):
    if len(lista) <= 1:
        return lista
    pivo = lista[0]
    maiores = []
    menores = []
    for i in range(1,len(lista)):
        if pivo[chave] > lista[i][chave]:
            menores.append(lista[i])
        else:
            maiores.append(lista[i])

    return quick_sort(menores, chave) + [pivo] + quick_sort(maiores, chave)

def binary_search(lista,chave_comparacao,chave_busca, item, inicio=0,fim=None):
    if fim is None:
        fim = len(lista)-1
    if inicio <= fim:
        meio = (inicio + fim)//2
        chute = lista[meio][chave_comparacao]
        if chute == item:
            return lista[meio][chave_busca]
        if chute < item:
            return binary_search(lista,chave_comparacao,chave_busca,item,meio+1,fim)
        else:
            return binary_search(lista,chave_comparacao,chave_busca,item, inicio,meio-1)
    else:
        return None

def validar_continuar(msg):
    while True:
        continuar = input(msg)
        if continuar in ['s','n']:
            return continuar
        print('responda entre (s ou n)!')

def validar_emergencia():
    lista_limite_acidentes = []
    while len(lista_limite_acidentes) < 3:
        try:
            with open('./arq_json/acidentes.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
        except IOError:
            print("Erro de IO (Entrada/Saída).")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}.")
        else:
            chaves = list(dados.keys())
            linha()
            for i in range(len(chaves)):
                print(f"{i + 1}. {chaves[i]}")
            linha()
            escolha_usuario = validar_int("Digite o número do tópico que deseja ver: ")
            linha()
            if escolha_usuario > 0 and escolha_usuario <= len(chaves):
                chave_selecionada = chaves[escolha_usuario-1]
                cabecalho(chave_selecionada)
                for i in range(len(dados[chave_selecionada])):
                    print(f'{i+1}. {dados[chave_selecionada][i]}')
                linha()
                escolha_usuario_2 = validar_int("Digite o número da emergência que deseja ver: ")

                if escolha_usuario_2 > 0 and escolha_usuario_2 <= len(dados[chave_selecionada]):
                    lista_limite_acidentes.append(dados[chave_selecionada][escolha_usuario_2-1])
                    print(lista_limite_acidentes)
                    contiuar = validar_continuar('deseja adicionar mais acidentes? (s/n): ')
                    if contiuar == 'n':
                        return lista_limite_acidentes
                else:
                    print("Número inválido!")
            else:
                print("Número inválido.")
    linha()
    print('limite de acidentes por chamada atingido')
    return lista_limite_acidentes

def assistente_emergencias(prompt_user):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt_sistema = """
    Você é um assistente virtual especializado em primeiros socorros. Vou lhe fazer algumas perguntas específicas e 
    preciso que suas respostas sejam breves, claras e informativas. Cada resposta deve ser limitada a no máximo 
    7 linhas, com quebras de linha adequadas para garantir a clareza na visualização do relatório.

    Formato de saída esperado:
    - Pergunta: [Insira a pergunta aqui]
    - Resposta: [Resposta concisa e informativa. Use '\n' para quebrar as linhas e manter a resposta dentro do limite 
    de 7 linhas.]

    """
    tentativas = 0
    tempo_exponencial = 5
    modelo = "gpt-3.5-turbo"
    codificador = tiktoken.encoding_for_model(modelo)
    lista_de_tokens = codificador.encode(prompt_sistema + prompt_user)
    tokens = len(lista_de_tokens)
    tamanho_esperado_saida = 2048
    if tokens > (4096 - tamanho_esperado_saida):
        modelo = "gpt-3.5-turbo-16k"
    while tentativas < 5:
        try:
            cabecalho('GERANDO RELATÓRIO ...')
            tentativas+=1
            response = openai.ChatCompletion.create(
                model=modelo,
                messages=[
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt_user
                    }
                ],
                temperature=1,
                max_tokens=tamanho_esperado_saida,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            resposta = response.choices[0].message.content
            return resposta
        except openai.error.AuthenticationError as e:
            print(f'ERRO DE AUTENTICAÇÃO: {e}')
        except openai.APIError as e:
            print(f'ERRO DE API: {e}')
            time.sleep(5)
        except openai.error.RateLimitError as e:
            print(f'ERRO LIMITE DE TAXA: {e}')
            time.sleep(tempo_exponencial)
            tempo_exponencial *= 2

def criar_arquivo(nome,conteudo,caminho):
    i = 1
    arq = caminho + nome
    nome_arquivo = arq + '.txt'
    while os.path.exists(nome_arquivo):
        cabecalho(f'{nome_arquivo} já encontrado')
        nome_arquivo = f'{arq}-{i}.txt'
        i+=1
    try:
        cabecalho(f'Criando arquivo {nome_arquivo}')
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f'Houve um erro: {e}')

def validar_doenca():
    while True:
        try:
            with open('./arq_json/doencas-cronicas.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
        except IOError:
            print("Erro de IO (Entrada/Saída).")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}.")
        else:
            for i, doenca_info in enumerate(dados):
                print(f'{i+1}. Doença: {doenca_info["doenca"]} - Descrição: {doenca_info["descricao"]}')
            opcao = validar_int('Digite o número da opção de doença que deseja: ')
            if opcao > 0 and opcao <= len(dados):
                return f'Doença: {dados[opcao-1]["doenca"]}, Descrição: {dados[opcao-1]["descricao"]}'
            else:
                print('Digite um número válido dentre as opções!')

def assistente_crise_doencas(prompt_user):
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt_sistema = """
        Você é um assistente virtual treinado em fornecer informações sobre gestão de doenças crônicas. Baseando-se em diretrizes médicas confiáveis, você fornecerá orientações claras e concisas sobre o que fazer durante uma crise aguda de uma doença crônica específica. Por favor, responda com recomendações práticas e passos de ação imediatos.

        Doença Crônica: [Nome da Doença]
        Tipo de Crise: [Descrição Breve da Crise]

        Instruções:
        1. Descreva os sinais de alerta que indicam que a pessoa está entrando em crise.
        2. Forneça uma lista de ações imediatas que a pessoa deve tomar assim que reconhecer esses sinais.
        3. Indique quando e como buscar ajuda médica.
        4. Ofereça conselhos sobre como gerenciar a crise até que a ajuda médica esteja disponível ou até que a crise seja resolvida.
        ##############
        Formato de saída desejado:
        - Sinais de Alerta: [Liste os sinais]
        - Ações Imediatas: [Liste as ações em bullet points]
        - Busca por Ajuda Médica: [Explique quando e como buscar ajuda]
        - Gerenciamento da Crise: [Forneça dicas de gerenciamento]
        """
    tentativas = 0
    tempo_exponencial = 5
    modelo = "gpt-3.5-turbo"
    codificador = tiktoken.encoding_for_model(modelo)
    lista_de_tokens = codificador.encode(prompt_sistema + prompt_user)
    tokens = len(lista_de_tokens)
    tamanho_esperado_saida = 2048
    if tokens > (4096 - tamanho_esperado_saida):
        modelo = "gpt-3.5-turbo-16k"
    while tentativas < 5:
        print(f' tentativa = {tentativas}')
        try:
            cabecalho('GERANDO RELATÓRIO ...')
            tentativas += 1
            response = openai.ChatCompletion.create(
                model=modelo,
                messages=[
                    {
                        "role": "system",
                        "content": prompt_sistema
                    },
                    {
                        "role": "user",
                        "content": prompt_user
                    }
                ],
                temperature=1,
                max_tokens=tamanho_esperado_saida,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            resposta = response.choices[0].message.content
            return resposta
        except openai.error.AuthenticationError as e:
            print(f'ERRO DE AUTENTICAÇÃO: {e}')
        except openai.APIError as e:
            print(f'ERRO DE API: {e}')
            time.sleep(5)
        except openai.error.RateLimitError as e:
            print(f'ERRO LIMITE DE TAXA: {e}')
            time.sleep(tempo_exponencial)
            tempo_exponencial *= 2


def validar_sintomas():
    while True:
        try:
            with open('./arq_json/sintomas.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("O arquivo não foi encontrado.")
        except IOError:
            print("Erro de IO (Entrada/Saída).")
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}.")
        else:
            for k,v in dados.items():
                linha()
                print(f'Tipo de sintoma: {k}')
                for j in v["sintomas"]:
                    print(j)
            linha()
            sintoma = input('Digite aqui qual tipo de sintoma se assemelha ao oque você apresenta: ').lower().strip()
            for key,value in dados.items():
                if sintoma == key:
                    linha()
                    print('Poissiveis Doenças:')
                    for i in value["condicoes"]:
                        print(f'-{i}')
                    linha()
                    continuar = validar_continuar('Deseja continuar? [s,n]: ').lower().strip()
                    if continuar == 'n':
                        return
            linha()
            print('Digite um sintoma válido! se atente com as acentuação! ')


