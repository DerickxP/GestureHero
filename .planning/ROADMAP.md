# Gesture Hero Roadmap

## O Que Já Foi Feito?
- Definida a visão do produto.
- Criada a especificação técnica dos gestos (open_hand, closed_fist, point_left, point_right).
- Configurado o ambiente virtual `GestureHero` com Python 3.12.
- Instaladas as dependências: OpenCV, MediaPipe, TensorFlow, Scikit-learn, etc.
- **[NOVO]** Criada a estrutura de containerização com `Dockerfile` e `.dockerignore`.

| ID | Phase | Responsibility | Scope | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| 1 | `Environment Setup` | Dev | Python 3.12, venv, dependencies, folders. | - | COMPLETED |
| 1.1 | `Dockerization` | Dev | Create Dockerfile and .dockerignore for portability. | Phase 1 | COMPLETED |
| 2 | `Data Collection (src/collect_data.py)` | Dev | Capture gesture landmarks (200 ea), save in `.npy`. | Phase 1 | TODO |
| 3 | `Preprocessing & Neural Network Training (src/train_model.py)` | AI | Normalize points (X,Y), build Keras Sequential model. | Phase 2 | TODO |
| 4 | `Game Loop & AI Inference (src/game.py)` | Dev/Game | OpenCV VideoLoop, HUD, Command logic, Scoring. | Phase 3 | TODO |
| 5 | `Final Polish & Portfolio Artifacts` | Portfolio | README.md, testing, visual cleanup. | Phase 4 | TODO |
