# FORMULA E SIMULATOR

## Alunos e RMs

- José Guilherme Sipaúba Costa - RM557274
- Fernando Navajas Moraes - RM555080
- Henrique Botti - RM556187
- Yuri Lopes Costa - RM555080

## Descrição do Projeto

O "FORMULA E SIMULATOR" é um jogo de corrida em Python utilizando a biblioteca Pygame. O jogo simula uma corrida de Fórmula E, onde o jogador controla um carro, devendo percorrer o circuito no menor tempo possível, desviando de obstáculos e completando voltas.

## Funcionalidades

- **Movimentação do Carro**: Controle completo sobre aceleração, desaceleração e rotação do carro.
- **Animações**: Animações de início e de game over para uma experiência mais imersiva.
- **Sistema de Dashes**: Permite ao jogador acelerar temporariamente ao passar por zonas específicas.
- **Sistema de Vidas**: O jogador começa com 5 vidas, perdendo uma ao colidir com as bordas da pista.
- **Sistema de Voltas**: O tempo de cada volta é registrado, e o melhor tempo é exibido ao final do jogo.
- **Música e Sons**: Música de fundo e efeitos sonoros durante o jogo.

## Instruções de Uso

### Executando o Jogo

1. Certifique-se de ter o Python instalado em sua máquina.
2. Instale a biblioteca Pygame utilizando o comando:

    ```bash
    pip install pygame
    ```

3. Coloque todas as imagens na pasta `imgs` dentro do diretório do projeto.
4. Execute o arquivo principal do jogo:

    ```bash
    python main.py
    ```

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
- `I` - Iniciar o jogo na tela de Início
- `Q` - Sair do jogo na tela de Game Over ou Finalizado
- `R` - Reiniciar o jogo na tela de Game Over ou Finalizado

### Objetivo do Jogo

Complete o maior número de voltas no menor tempo possível. O tempo de cada volta será registrado e exibido ao final do jogo, juntamente com o melhor tempo obtido.

## Requisitos

- Python 3.7 ou superior
- Pygame 2.0.0 ou superior

## Dependências

- Pygame

## Estrutura do Projeto

```bash
├── fonts/                  # Fonte utilizada no jogo
│   ├── PixelifySans-Bold.ttf
│   └── PixelifySans-Medium.ttf
├── imgs/                   # Contém todas as imagens do jogo (carros, pista, etc.)
├── sound/                  # Música de fundo do jogo
├── README.md               # Este arquivo
├── main.py                 # Arquivo principal contendo o código do jogo
├── players_data.json       # Arquivo de dados dos jogadores
└── utils.py                # Arquivo com funções auxiliares (ex: scale_image, blit_rotate_center)
```

## Detalhes Técnicos

### main.py

Arquivo principal do jogo. Contém a lógica do jogo, controle do carro, renderização das imagens e o loop principal.

### utils.py

Arquivo utilitário contendo funções auxiliares para manipulação de imagens e renderização.

### Funcionalidades

- **Carregamento de Imagens**: Carrega e escala as imagens utilizadas no jogo.
- **Criação da Janela do Jogo**: Define o tamanho da janela com base nas dimensões da pista.
- **Controle do Carro**: Classe `PlayerCar` controla a movimentação e colisão do carro do jogador.
- **Renderização**: Função `render` exibe as imagens na tela.
- **Movimentação do Jogador**: A função `move` controla a movimentação do carro do jogador com base nas teclas pressionadas.
- **Verificação de Colisões**: A função `collide` verifica colisões entre o carro e os obstáculos na pista.
- **Sistema de Voltas**: Registra o tempo de cada volta e exibe o melhor tempo ao final.
- **Animações**: Inclui animações para a tela inicial e para a tela de game over.
- **Redefinição de imagem**: A função `scale_image` redefine o tamanho da imagem multiplicando por um fator.
- **Rotação de imagem**: A função `blit_rotate_center` rotaciona a imagem pelo centro e exibe na tela.

## Informações Adicionais

O projeto é um jogo simples que permite ao jogador controlar um carro em uma pista de corrida, registrando o tempo de cada volta. O jogo ainda está em fase inicial, sem todas as funcionalidades finais, como competição com bots ou multiplayer. É uma ótima maneira de aprender as regras e conceitos da Fórmula E de forma interativa e divertida.

---

**Aproveite o jogo e tente bater o seu recorde!**
