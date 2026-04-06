# Gesture Hero Roadmap

## O Que Já Foi Feito?
- Definida a visão do produto.
- Criada a especificação técnica dos gestos (Open_Palm, Closed_Fist, Pointing_Up, Victory).
- Configurado o ambiente virtual `GestureHero` com Python 3.12.
- Instaladas as dependências: OpenCV, MediaPipe, etc.
- **[NOVO]** Criada a estrutura de containerização com `Dockerfile` e `.dockerignore`.
- **[NOVO]** Mudança para modelos pré-treinados do MediaPipe para evitar a fase de treinamento manual.

| ID | Phase | Responsibility | Scope | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| 1 | `Environment Setup` | Dev | Python 3.12, venv, dependencies, folders. | - | COMPLETED |
| 1.1 | `Dockerization` | Dev | Create Dockerfile and .dockerignore for portability. | Phase 1 | COMPLETED |
| 2 | `Pre-trained Model Setup` | Dev | Download `gesture_recognizer.task` e testar Task API. | Phase 1 | COMPLETED |
| 3 | `Game Logic & HUD (src/game.py)` | Dev/Game | VideoLoop, Inferência de Gestos, Score, HUD. | Phase 2 | TODO |
| 4 | `Final Polish & Portfolio Artifacts` | Portfolio | README.md, testes, limpeza visual. | Phase 3 | TODO |
