# Project: Gesture Hero

## 1. Visão do Produto
**Nome**: Gesture Hero
**Tipo**: Minigame com visão computacional em tempo real.
**Objetivo**: Criar um jogo controlado por gestos usando webcam, com detecção por MediaPipe e classificação por inteligência artificial (CNN/MLP).
**Finalidade**: Aprendizado prático de Visão Computacional, demonstração de portfólio e gameplay interativo.

## 2. Proposta do Jogo
O jogador executa gestos em frente à webcam para responder a comandos na tela:
- `mão aberta` (open_hand)
- `punho fechado` (closed_fist)
- `apontar para a esquerda` (point_left)
- `apontar para a direita` (point_right)

O sistema deve fornecer pontuação, sistema de combo, feedback visual e progresso de fase.

## 3. Stack Tecnológica
- **Linguagem**: Python 3.12 (Ambiente virtual `GestureHero`)
- **Bibliotecas**:
  - `OpenCV`: Captura de webcam e UI/HUD.
  - `MediaPipe`: Landmarks da mão (21 pontos).
  - `TensorFlow/Keras`: Modelo de classificação (IA).
  - `NumPy`, `Scikit-learn`: Manipulação de dados e métricas.

## 4. Arquitetura do Sistema
- **Captura**: Loop de vídeo via OpenCV.
- **Detecção**: MediaPipe extrai as coordenadas (X, Y, Z).
- **Classificador**: Rede Neural que decide qual o gesto com base nos pontos.
- **Motor do Jogo**: Lógica de comandos, score e tempo.
- **UI**: Overlays gráficos em tempo real.
