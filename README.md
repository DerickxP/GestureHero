*Read this in [English](README_EN.md).*

# Gesture Hero

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-5C3EE8?logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Gesture%20Recognizer-0097A7?logo=google&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

Minijogo de reflexo jogado com as mãos pela webcam: o jogo pede um gesto e você tem
alguns segundos para fazê-lo na frente da câmera. O reconhecimento usa o modelo
pré-treinado **Gesture Recognizer** do MediaPipe, então não há coleta de dados nem
treinamento: o jogo já funciona com o modelo incluído no repositório.

## Como funciona

1. A cada rodada o jogo sorteia um dos quatro gestos e mostra o nome na tela.
2. Cada quadro da webcam passa pelo Gesture Recognizer; se o gesto reconhecido for o
   pedido, você ganha **100 pontos** e a próxima rodada começa.
3. O tempo para responder começa em **3 s** e encolhe 3% a cada acerto, até o mínimo de
   **1,2 s**. Uma barra na parte de baixo mostra o tempo restante.
4. Deixar o tempo acabar custa uma das **3 vidas**. Sem vidas, aparece a tela de fim de
   jogo com a pontuação final.

## Gestos suportados

| Gesto | Nome no modelo | Comando na tela |
|---|---|---|
| ✋ Mão aberta | `Open_Palm` | MAO ABERTA |
| ✊ Mão fechada | `Closed_Fist` | MAO FECHADA |
| ✌️ Sinal de V | `Victory` | SINAL DE V |
| ☝️ Dedo para cima | `Pointing_Up` | DEDO P/ CIMA |

## Como rodar

Requisitos: Python 3.12 e uma webcam.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/game.py
```

Rode a partir da raiz do repositório, porque o modelo é lido de
`models/gesture_recognizer.task`. Se o arquivo não estiver lá, baixe com
`python scripts/download_model.py`.

Controles: **q** sai do jogo e **r** recomeça depois do fim de jogo.

## Estrutura

```
src/game.py                  # loop do jogo, regras e HUD desenhado com OpenCV
src/collect_data.py          # coleta de landmarks da mão em .npy (experimento, não usado pelo jogo)
scripts/download_model.py    # baixa o modelo do Gesture Recognizer
models/gesture_recognizer.task
Dockerfile, docker-compose.yml
```

## Limitações

- **Docker não testado de ponta a ponta.** A imagem inclui o modelo e as dependências,
  mas a configuração de vídeo (`DISPLAY=host.docker.internal:0.0` e `/dev/video0`) foi
  pensada para Windows com servidor X e precisa ser ajustada em outros sistemas. Rodar
  direto com Python é o caminho recomendado.
- O `requirements.txt` traz pacotes que o jogo não usa, como TensorFlow, Keras e
  scikit-learn, sobras do experimento de treinar um modelo próprio. Só `mediapipe`,
  `opencv-python` e `numpy` são necessários para jogar.
- Só a primeira mão detectada é considerada, e o reconhecimento depende de boa
  iluminação.

## Licença

[MIT](LICENSE)
