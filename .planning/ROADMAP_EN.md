# Gesture Hero Roadmap

## 🚀 Milestones

### **v1.0 - GestureHero (Current Phase)**
- ✅ Integrated MediaPipe recognition (no manual training required).
- ✅ Bilingual documentation and professional READMEs.
- ✅ Virtual environment `venv` configured and tracked.
- 🏁 **READY FOR PORTFOLIO.**

### **v1.1 - GestureHero - Docker (Next Phase)**
- [ ] Implement webcam passthrough for Docker on Windows (using usbipd-win).
- [ ] Optimize Docker image size.
- [ ] Automation with Docker Compose.

---

## What's been done?
- Product vision defined.
- Technical gesture specification created.
- **Pre-trained model (`gesture_recognizer.task`) already in the repo.**
- **Main game loop (`game.py`) fully functional.**

| ID | Phase | Responsibility | Scope | Status |
|:---|:---|:---|:---|:---|
| 1 | `Environment Setup` | Dev | Python 3.12, venv, dependencies, folders. | COMPLETED |
| 2 | `Pre-trained Model Setup` | Dev | MediaPipe Task API integration. | COMPLETED |
| 3 | `Bilingual Portfolio` | Portfolio | README, README_BR, Multi-language docs. | COMPLETED |
| 4 | `v1.1 - Docker Portability` | DevOps | Seamless webcam access via containers. | TODO |
