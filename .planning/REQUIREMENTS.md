# Requisitos do Gesture Hero

## 1. Funcionalidades Core (MVP)
- [ ] **Captura de Vídeo**: Abrir webcam com OpenCV em janela única.
- [ ] **Detector de Mãos**: Usar MediaPipe para encontrar 21 landmarks por mão.
- [ ] **Coleta de Dataset**: Script para salvar landmarks (X, Y) em CSV/npy para treinamento.
- [ ] **Inteligência Artificial (Modelo)**: Rede neural treinada para classificar 4 gestos:
  - `open_hand`, `closed_fist`, `point_left`, `point_right`.
- [ ] **Lógica de Jogo**:
  - Timer por rodada.
  - Comandos aleatórios.
  - Sistema de pontuação e combo.
  - Feedback visual (correta/errada).

## 2. Requisitos Técnicos
- **Python Version**: 3.12 (Obrigatório para compatibilidade TensorFlow).
- **HUD (Interface)**: Overlays em tempo real sobre o frame do OpenCV.
- **Inferência**: O loop de detecção deve rodar rápido o suficiente para ser jogável (~20-30 FPS).
