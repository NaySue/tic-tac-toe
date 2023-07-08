
# Jogo da Velha (tic tac toe)

## Descrição
O Jogo da Velha é um jogo clássico para dois jogadores jogado em uma grade 3x3. O objetivo é conseguir três de seus símbolos (X ou O) em uma linha, coluna ou diagonal.

## Instalação
- É necessário ter o Python 3.x para executar o jogo.
- Clone o repositório para sua máquina local.
- Instale as dependências necessárias usando pip install -r requirements.txt.

## Uso
- Execute o jogo usando o comando python tic_tac_toe.py.
- Use as teclas numéricas (1-9) para fazer suas jogadas no tabuleiro.
- Pressione 'q' para sair do jogo.

## Regras do Jogo
- Os jogadores fazem jogadas alternadamente marcando uma célula no tabuleiro.
- O primeiro jogador a obter três de seus símbolos em uma linha, coluna ou diagonal vence.
- Se todas as células estiverem preenchidas e nenhum jogador vencer, o jogo termina em empate.

## Detalhes de Implementação
- O jogo é implementado em Python utilizando a biblioteca curses para a interface de usuário no console.
- O algoritmo minimax é usado para determinar as jogadas do computador.
- Os estados do jogo são representados usando uma estrutura de árvore.
- A busca em largura (BFS), ou busca em profundidade (DFS), é utilizada para gerar os estados do jogo.

## Contribuições
- Contribuições são bem-vindas! Faça um fork do repositório e envie um pull request.
