import urllib.request
import os

def download_model():
    """Baixa o modelo pré-treinado da Google para reconhecimento de gestos"""
    
    # URL oficial do modelo MediaPipe (Google AI)
    # Este arquivo .task contém a rede neural que reconhece os pontos das mãos.
    model_url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
    
    # Caminho onde o arquivo será salvo localmente
    save_path = os.path.join("models", "gesture_recognizer.task")

    # Garante que a pasta 'models' exista, se não, ela é criada automaticamente.
    os.makedirs("models", exist_ok=True)

    print(f"Iniciando o download do modelo para: {save_path}...")
    try:
        # Baixa o arquivo da internet usando a biblioteca padrão do Python
        urllib.request.urlretrieve(model_url, save_path)
        print("Download concluído com sucesso!")
        print("Agora você já pode rodar o Gesture Hero!")
    except Exception as e:
        # Caso ocorra algum erro (conexão, permissão, etc.), ele será exibido aqui.
        print(f"Erro ao baixar o modelo de IA: {e}")

if __name__ == "__main__":
    download_model()
