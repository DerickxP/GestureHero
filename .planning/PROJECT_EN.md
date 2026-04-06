# Project: Gesture Hero

## 1. Product Vision
**Name**: Gesture Hero
**Type**: Real-time Computer Vision Minigame.
**Objective**: Create a gesture-controlled game using a webcam, with MediaPipe detection and pre-trained classification models.
**Purpose**: Practical learning of Computer Vision, portfolio demonstration, and interactive gameplay.

## 2. Game Proposal
The player performs gestures in front of the webcam to respond to screen commands:
- `Open_Palm` (Defense or Menu)
- `Closed_Fist` (Attack or Select)
- `Victory` (Special Move)
- `Pointing_Up` (Navigate/Aim)

The system provides scoring, a combo system, visual feedback, and level progress.

## 3. Tech Stack
- **Language**: Python 3.12 (Virtual Environment `GestureHero`)
- **Libraries**:
  - `OpenCV`: Webcam capture and UI/HUD.
  - `MediaPipe`: Pre-trained gestures (Gesture Recognizer API).
  - `NumPy`: Matrix and vector manipulation.

## 4. System Architecture
- **Capture**: Video Loop via OpenCV.
- **Detection & Classification**: MediaPipe Tasks analyzes hands and classifies gestures natively.
- **Game Engine**: Command logic, score, and timer based on detected gestures.
- **UI**: Real-time graphic overlays (HUD).
