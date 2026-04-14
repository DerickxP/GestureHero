*🌍 Leia em [Português](README.md).*

# 🖐️ Gesture Hero

**Gesture Hero** is a real-time computer vision minigame where you control the action using hand gestures. Built with Python, OpenCV, and Google's MediaPipe, it demonstrates the power of pre-trained AI models in interactive applications.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-green.svg)
![OpenCV](https://img.shields.io/badge/UI-OpenCV-orange.svg)
![Docker](https://img.shields.io/badge/Environment-Docker-blue.svg)

## 🎯 Project Vision
The goal of this project is to create an engaging, low-latency gaming experience using nothing but a standard webcam. By leveraging **MediaPipe's Gesture Recognizer API**, we achieve high-precision detection without the need for custom dataset collection or manual model training.

## ✨ Features
- **Real-time Recognition**: Instant detection of complex hand gestures.
- **Pre-trained AI**: Uses Google's state-of-the-art gesture recognition models.
- **Portable**: Fully containerized with Docker for consistent deployment.
- **Professional Architecture**: Managed with professional software development practices.

## 🚀 Supported Gestures
| Gesture | Game Action |
|:---|:---|
| 🖐️ **Open_Palm** | Defense / Menu |
| ✊ **Closed_Fist** | Attack / Select |
| ✌️ **Victory** | Special Move |
| ☝️ **Pointing_Up** | Navigate / Aim |

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12+
- A working webcam

### Local Setup
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd GestureHero
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv GestureHero
   .\GestureHero\Scripts\activate  # Windows
   source GestureHero/bin/activate # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requeriments.txt
   ```

4. **Run the Game:**
   ```bash
   python src/game.py
   ```

### Docker Setup
If you prefer to run in a containerized environment (for development setup):
```bash
docker build -t gesture-hero .
```

## 📂 Project Structure
- `src/`: Main source code (Game loop and logic).
- `models/`: Pre-trained AI model files (`.task`).
- `scripts/`: Utility scripts (model downloaders, etc.).
- `.planning/`: Documentation and project lifecycle management.

---
*Created with ❤️ for portfolio demonstration purposes.*
