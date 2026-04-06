# 1. Usar a imagem oficial do Python 3.12 (leve)
FROM python:3.12-slim

# 2. Instalar dependências do sistema para o OpenCV funcionar no Linux
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Definir a pasta de trabalho dentro do container
WORKDIR /app

# 4. Copiar o arquivo de requisitos e instalar as bibliotecas
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt

# 5. Copiar o resto do código fonte
COPY . .

# 6. Comando para rodar o app (ajustaremos depois para a fase de jogo)
CMD ["python", "src/collect_data.py"]
