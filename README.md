# FORMULA E SIMULATOR

## Alunos e RMs

- José Guilherme Sipaúba Costa - RM557274
- Fernando Navajas Moraes - RM555080
- Henrique Botti - RM556187
- Yuri Lopes Costa - RM555080

## Descrição do Projeto

O "FORMULA E SIMULATOR" é um jogo de corrida em Python utilizando a biblioteca Pygame. O jogo simula uma corrida de Fórmula E onde o jogador controla um carro, devendo percorrer o circuito no menor tempo possível, desviando de obstáculos e completando voltas.

## Instruções de Uso

### Executando o Jogo

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale a biblioteca Pygame utilizando o comando:
    
    `pip install pygame`
    
3. Coloque todas as imagens na pasta `imgs` dentro do diretório do projeto.
4. Execute o arquivo principal do jogo:
    
    `python main.py`
    
5. Digite seu nome quando solicitado e controle o carro utilizando as seguintes teclas:
    - `W` para mover para frente
    - `S` para mover para trás
    - `A` para girar para a esquerda
    - `D` para girar para a direita

### Controles do Jogo

- `W` - Acelerar
- `S` - Ré
- `A` - Girar para a esquerda
- `D` - Girar para a direita

### Objetivo do Jogo

Complete o maior número de voltas no menor tempo possível. O tempo de cada volta será registrado e exibido ao final do jogo, juntamente com o melhor tempo obtido.

## Requisitos

- Python 3.7 ou superior
- Pygame 2.0.0 ou superior

## Dependências

- Pygame

## Estrutura do Projeto

```
├── imgs/
│   ├── bg.png 
│   ├── track2.png 
│   ├── border2.png 
│   ├── finish2.png 
│   ├── racecar.png 
│   └── green-car.png 
├── utils.py 
└── main.py
```

## Detalhes Técnicos

### main.py

Arquivo principal do jogo. Contém a lógica do jogo, controle do carro, renderização das imagens e o loop principal.

### utils.py

Arquivo utilitário contendo funções auxiliares para manipulação de imagens e renderização.

## Funcionalidades

- **Carregamento de Imagens**: Carrega e escala as imagens utilizadas no jogo.
- **Criação da Janela do Jogo**: Define o tamanho da janela com base nas dimensões da pista.
- **Controle do Carro**: Classe `AbstractCar` controla a movimentação e colisão dos carros. Classe `PlayerCar` especializa o comportamento do carro controlado pelo jogador.
- **Renderização**: Função `render` exibe as imagens na tela.
- **Movimentação do Jogador**: Função `move_player` controla a movimentação do carro do jogador com base nas teclas pressionadas.
- **Verificação de Colisões**: Função `collide` verifica colisões entre o carro e os obstáculos.
- **Sistema de Voltas**: Registra o tempo de cada volta e exibe o melhor tempo ao final.
- **Redefinição de imagem**: Função `scale_image` redefine o tamanho da imagem multiplicando por um fator.
- **Rotação de imagem**: Função `blit_rotate_center` rotaciona a imagem pelo centro e exibe na tela.

## Informações Adicionais

O projeto até agora é um jogo simples que permite ao jogador controlar um carro em uma pista de corrida, registrando o tempo de cada volta. O jogo ainda se apresenta na fase inicial, não possuindo todas as funcionalidades finais, como competição com bots, multiplayer e habilidades como Attack Mode, refletindo a competição da Fórmula E. É uma ótima oportunidade para aprender as regras e conceitos da Fórmula E, de uma maneira fluída e intuitiva.