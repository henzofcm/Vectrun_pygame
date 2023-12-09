# Vectrun

Bem-vindo(a) ao Vectrun, um jogo que oferece uma abordagem inovadora para o ensino de vetores no plano, onde os jogadores têm a oportunidade de manipular uma moto através de vetores no plano cartesiano.

## Descrição do Jogo

O jogo Vectrun possui dois modos: The Grid (Arena) e The Trench (Trincheira). No primeiro, todos os jogadores disputam entre si dentro de uma arena, o objetivo é ser o último sobrevivente. Já no outro modo, eles disputam uma corrida com obstáculos, podendo um jogador interferir na corrida do outro.

### The Grid

1. As Cartas de Vetores são embaralhadas automaticamente. Cada jogador recebe 3 cartas de vetores, e elas são exibidas apenas para o próprio jogador, mantendo-se ocultas dos outros participantes. As cartas restantes são armazenadas em uma pilha.
2. As motos dos jogadores começam na origem do plano cartesiano, no ponto (0, 0)
3. Cada jogador está autorizado a usar uma Carta de Vetor por jogada para realizar um movimento. Esse movimento deve ser executado de acordo com uma das 3 Cartas de Vetores disponíveis.
4. Após a realização do movimento, o jogo marca o deslocamento no tabuleiro com uma linha. A carta utilizada é automaticamente descartada, e uma nova carta é retirada da pilha de Cartas de Vetores.
5. O jogo continua com cada jogador realizando seus movimentos. Em algum momento no jogo, uma das seguintes Ações Críticas poderá ocorrer: 



![](./assets/manual/img/colission_with_side_walls.png) | ![](./assets/manual/img/intersection_with_the_line.png) | ![](./assets/manual/img/intersection_with_motorcycle.png)
:--------------------------------------: |:--------------------------------------: |:--------------------------------------:
Colisão com Paredes Laterais | Interseção com linha | Interseção com moto

### The Trench

![](./assets/manual/img/scalar_acceleration.png) | ![](./assets/manual/img/intersection_with_red_aircraft.png) | ![](./assets/manual/img/wall_with_glich.png)
:--------------------------------------: |:--------------------------------------: |:--------------------------------------:
Aceleração por escalar | Interseção com moto |  Parede com glitch




## Como Jogar

### Controles

### Objetivo

## Requisitos

- Python 3
- Pygame (instalado via `pip install pygame`)

## Como Executar

1. Clone este repositório em sua máquina local


2. Navegue até o diretório do jogo


3. Execute o jogo


## Créditos

- Idealizado por Tulio.
- Desenvolvido por Beatriz, Gustavo e Henzo.

