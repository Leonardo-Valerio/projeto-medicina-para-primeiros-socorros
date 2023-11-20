from funcoes_de_menu import *


opcoes_cadastro=['CADASTRAR', 'FAZER LOGIN', 'ENTRAR SEM LOGIN']

acesso = cadastro(opcoes_cadastro)

opcoes_menu = ['HOSPITAIS MAIS PERTOS DE MIM','CONSULTOR DE EMERGÊNCIAS MÉDICAS', 'SAIR']

while True:
    linha()
    exibir_menu(opcoes_menu)
    linha()
    opcao = validar_int('Digite a opção que deseja: ')
    if opcao == 1:
        cabecalho(opcoes_menu[0])
        if acesso != []:
            while True:
                pergunta = validar_int('Você deseja utilizar o seu cep do cadastro para a busca, ou deseja digitar um outro? (1 para cep de cadastro, 2 para outro cep) ')
                if pergunta == 1:
                    cep = buscar_cep_usuario(acesso["nome"])
                    print(cep)
                    break
                elif pergunta == 2:
                    numero_casa = validar_int('Digite o número da sua casa: ')
                    cep = encontrar_cep('digite o seu CEP (apenas números nesse campo): ', numero_casa)
                    break
                else:
                    cabecalho('Digite entre 1 e 2!')
        else:
            cep = encontrar_cep('digite o seu CEP (apenas números nesse campo): ')
        resultado = puxar_coordenadas(cep,api_key)
        hospitais = find_hospitals(resultado["lat"], resultado["lng"], api_key,2000)
    elif opcao == 2:
        cabecalho(opcoes_menu[1])
        acidentes = validar_emergencia()
        print(acidentes)
    elif opcao == 3:
        cabecalho('SAINDO...')
        break
    else:
        cabecalho('DIGITE UMA OPÇÃO VÁLIDA!')

