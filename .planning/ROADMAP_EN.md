# Gesture Hero Roadmap

## What's been done?
- Product vision defined.
- Technical gesture specification created (Open_Palm, Closed_Fist, Pointing_Up, Victory).
- `GestureHero` virtual environment (Python 3.12) configured.
- Dependencies installed: OpenCV, MediaPipe, etc.
- **[NEW]** Containerization structure created with `Dockerfile` and `.dockerignore`.
- **[NEW]** Switched to MediaPipe Pre-trained Models to skip custom training phase.

| ID | Phase | Responsibility | Scope | Depends on | Status |
|:---|:---|:---|:---|:---|:---|
| 1 | `Environment Setup` | Dev | Python 3.12, venv, dependencies, folders. | - | COMPLETED |
| 1.1 | `Dockerization` | Dev | Create Dockerfile and .dockerignore for portability. | Phase 1 | COMPLETED |
| 2 | `Pre-trained Model Setup` | Dev | Download `gesture_recognizer.task` and test Task API. | Phase 1 | COMPLETED |
| 3 | `Game Logic & HUD (src/game.py)` | Dev/Game | VideoLoop, Gesture Inference, Score, HUD. | Phase 2 | TODO |
| 4 | `Final Polish & Portfolio Artifacts` | Portfolio | README.md, testing, visual cleanup. | Phase 3 | TODO |
