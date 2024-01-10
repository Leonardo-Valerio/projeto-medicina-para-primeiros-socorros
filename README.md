# Health Guardian - Auxílio Emergencial Integrado

## Descrição Geral

O Health Guardian é um programa projetado para fornecer assistência em situações de emergência médica, oferecendo uma variedade de funcionalidades,
desde encontrar hospitais próximos até fornecer auxílio em acidentes comuns, suporte em crises de doenças e avaliação de sintomas para sugestões de possíveis doenças.

## Funcionalidades

1. **Cadastro e Login de Usuário:**
   - Os usuários podem realizar cadastro, fazer login ou usar o programa sem login.
   - O login permite acesso a informações armazenadas, como nome e endereço, otimizando a experiência do usuário.

2. **Encontrar Hospitais nas Proximidades:**
   - Os usuários podem inserir seu CEP ou utilizar o salvo no perfil.
   - Utiliza a API do Google Maps para localizar hospitais próximos à localização fornecida.

3. **Assistente de Emergência:**
   - Ajuda em acidentes comuns, fornecendo relatórios gerados por uma API de chat baseada em GPT.
   - Responde até três perguntas relacionadas ao acidente para orientação rápida.

4. **Auxílio em Crises de Doenças:**
   - Oferece assistência para crises relacionadas a doenças comuns.
   - Gera relatórios detalhados com instruções e guias passo a passo utilizando a API de chat baseada em GPT.

5. **Avaliação de Sintomas:**
   - Permite aos usuários avaliar sintomas selecionando tipos específicos.
   - Gera uma lista de possíveis doenças relacionadas aos sintomas selecionados.

6. **Sair do Programa:**
   - Oferece a opção de encerrar o programa quando o usuário conclui o uso das funcionalidades.

7. **Validações:**
   - Todas as validações, tratamento de erros, busca, geração de arquivos e comparações estão organizadas em funções nos arquivos `funcoes_de_cadastro` e `funcoes_de_menu`.

## APIs Utilizadas
- API OpenAi Chat-GPT
- API Google Maps
  
## Algoritmos Adicionais
Além das funcionalidades principais, incorporei algoritmos como QuickSort e Binary Search para otimizar algumas operações, como buscar o CEP de um usuário.

## Link do vídeo explicando e demonstrando o funcionamento do código que desenvolvi
https://youtu.be/D0rkYnnJfX4?si=9InxQCwJb6827KSU
