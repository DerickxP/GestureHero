# Projeto: Gesture Hero

## 1. Visão do Produto
**Nome**: Gesture Hero
**Tipo**: Minigame com visão computacional em tempo real.
**Objetivo**: Criar um jogo controlado por gestos usando webcam, com detecção por MediaPipe e modelos de classificação pré-treinados.
**Finalidade**: Aprendizado prático de Visão Computacional, demonstração de portfólio e gameplay interativo.

## 2. Proposta do Jogo
O jogador executa gestos em frente à webcam para responder a comandos na tela:
- `Open_Palm` (Defesa ou Menu)
- `Closed_Fist` (Ataque ou Seleção)
- `Victory` (Especial)
- `Pointing_Up` (Navegação/Mira)

O sistema deve fornecer pontuação, sistema de combo, feedback visual e progresso de fase.

## 3. Stack Tecnológica
- **Linguagem**: Python 3.12 (Ambiente virtual `GestureHero`)
- **Bibliotecas**:
  - `OpenCV`: Captura de webcam e UI/HUD.
  - `MediaPipe`: Gestos pré-treinados (Gesture Recognizer API).
  - `NumPy`: Manipulação de matrizes e vetores.

## 4. Arquitetura do Sistema
- **Captura**: Loop de vídeo via OpenCV.
- **Detecção & Classificação**: MediaPipe Tasks analisa as mãos e classifica o gesto nativamente (pré-treinado).
- **Motor do Jogo**: Lógica de comandos, score e tempo com base no gesto detectado.
- **UI**: Overlays gráficos em tempo real (HUD).
