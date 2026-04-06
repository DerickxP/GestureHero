# 🖐️ Gesture Hero

**Gesture Hero** é um minijogo de visão computacional em tempo real onde você controla a ação usando gestos das mãos. Construído com Python, OpenCV e MediaPipe do Google, ele demonstra o poder de modelos de IA pré-treinados em aplicações interativas.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![MediaPipe](https://img.shields.io/badge/AI-MediaPipe-green.svg)
![OpenCV](https://img.shields.io/badge/UI-OpenCV-orange.svg)
![Docker](https://img.shields.io/badge/Ambiente-Docker-blue.svg)

## 🎯 Visão do Projeto
O objetivo deste projeto é criar uma experiência de jogo envolvente e de baixa latência usando nada mais do que uma webcam padrão. Ao aproveitar a **Gesture Recognizer API do MediaPipe**, alcançamos detecção de alta precisão sem a necessidade de coleta de dataset customizado ou treinamento manual de modelos.

## ✨ Funcionalidades
- **Reconhecimento em Tempo Real**: Detecção instantânea de gestos complexos das mãos.
- **IA Pré-treinada**: Utiliza os modelos de reconhecimento de gestos de última geração do Google.
- **Portátil**: Totalmente conteinerizado com Docker para implantação consistente.
- **Arquitetura Profissional**: Gerenciado com práticas profissionais de ML.

## 🚀 Gestos Suportados
| Gesto | Ação no Jogo |
|:---|:---|
| 🖐️ **Open_Palm** | Defesa / Menu |
| ✊ **Closed_Fist** | Ataque / Seleção |
| ✌️ **Victory** | Movimento Especial |
| ☝️ **Pointing_Up** | Navegação / Mira |

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.12+
- Uma webcam funcional

### Configuração Local
1. **Clone o repositório:**
   ```bash
   git clone <url-do-seu-repositorio>
   cd GestureHero
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv GestureHero
   .\GestureHero\Scripts\activate  # Windows
   source GestureHero/bin/activate # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requeriments.txt
   ```

4. **Execute o Jogo:**
   ```bash
   python src/game.py
   ```

### Configuração Docker
Se preferir rodar em um ambiente conteinerizado:
```bash
docker build -t gesture-hero .
```

## 📂 Estrutura do Projeto
- `src/`: Código-fonte principal (Loop e lógica do jogo).
- `models/`: Arquivos de modelo de IA pré-treinados (`.task`).
- `scripts/`: Scripts utilitários (downloaders de modelos, etc.).
- `.planning/`: Documentação e gerenciamento do ciclo de vida do projeto.

---
*Criado com ❤️ para fins de demonstração de portfólio.*
