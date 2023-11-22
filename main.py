from funcoes_de_menu import *


opcoes_cadastro=['CADASTRAR', 'FAZER LOGIN', 'ENTRAR SEM LOGIN']

acesso = cadastro(opcoes_cadastro)

opcoes_menu = ['HOSPITAIS MAIS PERTOS DE MIM','ASSISTENTE DE EMERGÊNCIAS MÉDICAS','ASSISTENTE DE CRISES DE DOENÇAS','AVALIADOR DE SINTOMAS', 'SAIR']

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
                    cep = encontrar_cep('digite o seu CEP (apenas números nesse campo): ')
                    break
                else:
                    cabecalho('Digite entre 1 e 2!')
        else:
            cep = encontrar_cep('digite o seu CEP (apenas números nesse campo): ')
        resultado = puxar_coordenadas(cep,api_key)
        hospitais = encontrar_hospitais(resultado["lat"], resultado["lng"], api_key,2000)
    elif opcao == 2:
        if acesso != []:
            cabecalho(opcoes_menu[1])
            acidentes = validar_emergencia()
            relatorio = assistente_emergencias(f'{acidentes}')
            criar_arquivo(acesso["nome"], relatorio, './arquivos-assistente-emergencias/assistente-emergencias-')
        else:
            cabecalho('FAÇA SEU LOGIN PARA ACESSAR ESSA FUNCIONALIDADE')
            acesso = cadastro(opcoes_cadastro)
    elif opcao == 3:
        if acesso != []:
            cabecalho(opcoes_menu[2])
            doenca = validar_doenca()
            cabecalho(doenca)
            relatorio = assistente_crise_doencas(doenca)
            print(relatorio)
            criar_arquivo(acesso["nome"], relatorio, './arquivos-assistente-crises-doencas/assistente-crises-emergenciais-')
        else:
            cabecalho('FAÇA SEU LOGIN PARA ACESSAR ESSA FUNCIONALIDADE')
            acesso = cadastro(opcoes_cadastro)
    elif opcao == 4:
        cabecalho(opcoes_menu[3])
        validar_sintomas()
    elif opcao == 5:
        cabecalho('SAINDO...')
        break
    else:
        cabecalho('DIGITE UMA OPÇÃO VÁLIDA!')

