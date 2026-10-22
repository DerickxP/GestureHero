*Leia em [Português](README.md).*

# Gesture Hero

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-5C3EE8?logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Gesture%20Recognizer-0097A7?logo=google&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

A reflex minigame played with your hands through the webcam: the game asks for a
gesture and you have a few seconds to make it in front of the camera. Recognition uses
MediaPipe's pre-trained **Gesture Recognizer** model, so there is no data collection or
training: the game works out of the box with the model included in the repository.

## How it works

1. Each round the game picks one of the four gestures at random and shows its name on
   screen.
2. Every webcam frame goes through the Gesture Recognizer; if the recognized gesture is
   the requested one, you earn **100 points** and the next round starts.
3. The time to respond starts at **3 s** and shrinks by 3% on each hit, down to a minimum
   of **1.2 s**. A bar at the bottom shows the time left.
4. Letting the time run out costs one of your **3 lives**. With no lives left, the game
   over screen shows the final score.

## Supported gestures

| Gesture | Model label | On-screen command (PT) |
|---|---|---|
| ✋ Open hand | `Open_Palm` | MAO ABERTA |
| ✊ Closed fist | `Closed_Fist` | MAO FECHADA |
| ✌️ Victory sign | `Victory` | SINAL DE V |
| ☝️ Pointing up | `Pointing_Up` | DEDO P/ CIMA |

## How to run

Requirements: Python 3.12 and a webcam.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/game.py
```

Run it from the repository root, because the model is loaded from
`models/gesture_recognizer.task`. If the file is missing, download it with
`python scripts/download_model.py`.

Controls: **q** quits and **r** restarts after game over.

## Structure

```
src/game.py                  # game loop, rules and HUD drawn with OpenCV
src/collect_data.py          # hand landmark collection to .npy (experiment, not used by the game)
scripts/download_model.py    # downloads the Gesture Recognizer model
models/gesture_recognizer.task
Dockerfile, docker-compose.yml
```

## Limitations

- **Docker does not work yet.** The `Dockerfile` copies `requeriments.txt`, but the file
  is named `requirements.txt`, and `.dockerignore` excludes the `models/` folder. The
  video setup (`DISPLAY=host.docker.internal:0.0` and `/dev/video0`) also targets Windows
  with an X server and needs adjusting on other systems.
- `requirements.txt` includes packages the game does not use, such as TensorFlow, Keras
  and scikit-learn, left over from an experiment with training a custom model. Only
  `mediapipe`, `opencv-python` and `numpy` are needed to play.
- Only the first detected hand is considered, and recognition depends on good lighting.

## License

[MIT](LICENSE)
