# Gesture Hero Roadmap

## 🚀 Milestones (Marcos)

### **v1.0 - GestureHero (Atual)**
- ✅ Reconhecimento MediaPipe integrado (sem treinamento manual).
- ✅ Documentação bilíngue e README profissional.
- ✅ Ambiente virtual `venv` configurado e documentado.
- 🏁 **PRONTO PARA O PORTFÓLIO.**

### **v1.1 - GestureHero - Docker (Próximo)**
- [ ] Implementar webcam passthrough para Docker no Windows (via usbipd-win).
- [ ] Otimização da imagem Docker para redução de tamanho.
- [ ] Automação de instação via Docker Compose.

---

## O Que Já Foi Feito?
- Definida a visão do produto.
- Criada a especificação técnica dos gestos.
- **Modelo pré-treinado (`gesture_recognizer.task`) já no repositório.**
- **Loop principal de jogo (`game.py`) funcional.**

| ID | Phase | Responsibility | Scope | Status |
|:---|:---|:---|:---|:---|
| 1 | `Environment Setup` | Dev | Python 3.12, venv, dependencies, folders. | COMPLETED |
| 2 | `Pre-trained Model Setup` | Dev | MediaPipe Task API integration. | COMPLETED |
| 3 | `Bilingual Portfolio` | Portfolio | README, README_BR, Multi-language docs. | COMPLETED |
| 4 | `v1.1 - Docker Portability` | DevOps | Seamless webcam access via containers. | TODO |
