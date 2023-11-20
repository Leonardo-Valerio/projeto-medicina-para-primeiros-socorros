from funcoes_de_cadastro import *
import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('MAPS_API_KEY')
def puxar_coordenadas(cep,api_key):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={cep}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        resposta = response.json()
        localizacao = resposta["results"][0]["geometry"]["location"]
        return localizacao

def find_hospitals(latitude, longitude, api_key,area):
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
            find_hospitals(latitude,longitude,api_key,area)
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


