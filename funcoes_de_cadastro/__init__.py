import json
import requests


def linha():
    print('-' * 100)

def cabecalho(msg):
    linha()
    print(msg.center(100))
    linha()

def exibir_menu(lista):
    for i in range(len(lista)):
        print(f'{i+1} - {lista[i]}')

def validar_int(n):
    while True:
        try:
            num = int(input(n))
        except:
            print('Digite um número válido!!!')
        else:
            return num



def fazer_cadastro(nome, senha, cep):
    nome_arquivo = './arquivo_cadastros/cadastros.json'
    novo_usuario = {
        "nome": nome,
        "senha": senha,
        "cep": cep["cep"],
        "estado": cep["uf"],
        "bairro": cep["bairro"],
        "rua": cep["logradouro"],
        "numero": cep["numero"]
    }

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        dados.append(novo_usuario)

        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4)
        cabecalho('CADASTRO REALIZADO COM SUCESSO!')
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}.")



def validar_user(nome):
    try:
        with open('./arquivo_cadastros/cadastros.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}.")
    else:
        while True:
            liberar_usuario = True
            name = input(nome)
            if name.isalpha() and len(name) >= 3:
                for usuario in dados:
                    if name == usuario["nome"]:
                        print('ERRO, usuário já existente, digite outro')
                        liberar_usuario = False
                        break
                if liberar_usuario:
                    return name
            else:
                print('digite um nome válido, com pelo menos 3 dígitos, utilize apenas letras no nome! ')

def validar_senha(password, usuario):
    while True:
        try:
            senha = input(password)
            if senha.isalnum() and len(senha) >5 and senha != usuario:
                return senha
            else:
                print('digite uma senha válida, com mais de 5 dígitos e que não pode ser igual ao seu nome de usuário!')
        except IOError as e:
            print(f'ERRO: {e}')

def encontrar_cep(num_cep, num_casa=0):
    while True:
        cep = input(num_cep)
        if len(cep) != 8:
            print('digite um cep existente!')
        else:
            try:
                respose = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
                if respose.status_code == 200:
                    endereco = respose.json()
                    if num_casa > 0:
                        endereco['numero'] = num_casa
                    return endereco
                else:
                    print('CEP inválido')
            except Exception as e:
                print(f'Ocorreu um erro: {e}')




def fazer_login(name,password):
    try:
        with open('./arquivo_cadastros/cadastros.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}.")
    else:
        while True:
            nome = input(name).lower()
            senha = input(password).lower()
            for i in dados:
                if nome == i["nome"] and senha == i["senha"]:
                    return {"nome": nome, "senha": senha}
            print('Nome ou senha incorretos!')
            return []


def cadastro(menu_cadastro):
    while True:
        cabecalho('ENTRE COM SUA CONTA')
        linha()
        exibir_menu(menu_cadastro)
        linha()
        opcao = validar_int('Digite a opção que deseja: ')
        if opcao == 1:
            cabecalho(menu_cadastro[0])
            novo_nome = validar_user('digite seu nome: ')
            nova_senha = validar_senha('crie sua senha: ',novo_nome)
            numero_casa = validar_int('digite o número da sua residência: ')
            cep = encontrar_cep('digite o seu CEP (apenas números nesse campo): ', numero_casa)
            fazer_cadastro(novo_nome,nova_senha,cep)
        elif opcao == 2:
            cabecalho(menu_cadastro[1])
            acesso = fazer_login('digite seu nome: ','digite sua senha: ')
            if acesso != []:
                cabecalho('Login realizado com sucesso!')
                cabecalho(f'SEJA BEM VINDO {acesso["nome"].upper()}!')
                return acesso
        elif opcao == 3:
            cabecalho(menu_cadastro[2])
            acesso = []
            cabecalho('SEJA BEM VINDO!')
            return acesso
        else:
            print('Digite um número dentre as opções acima!')