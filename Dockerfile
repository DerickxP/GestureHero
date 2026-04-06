# 1. Definimos a Imagem Base (O "computador limpo" com Python já instalado)
FROM python:3.12-slim

# 2. Instalamos as dependências do Sistema Operacional (Debian Linux)
# O OpenCV precisa dessas bibliotecas específicas (libgl1, libglib2.0) para "desenhar" na tela.
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Definimos a pasta de trabalho (Onde o seu código vai morar no container)
WORKDIR /app

# 4. Copiamos o seu arquivo de requerimentos e instalamos as bibliotecas do Python
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt

# 5. Copiamos o restante do seu projeto para dentro do container
COPY . .

# 6. Definimos uma variável de ambiente padrão para o "Display" (Tela)
# O hospedeiro Windows (sua máquina) terá o IP configurado aqui depois.
ENV DISPLAY=host.docker.internal:0.0

# 7. Comando de Inicialização (O que o computador faz assim que liga)
CMD ["python", "src/game.py"]
