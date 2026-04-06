import urllib.request
import os

def download_model():
    model_url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
    save_path = os.path.join("models", "gesture_recognizer.task")

    # Garante que a pasta models existe
    os.makedirs("models", exist_ok=True)

    print(f"Iniciando o download do modelo para: {save_path}...")
    try:
        urllib.request.urlretrieve(model_url, save_path)
        print("Download concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar o modelo: {e}")

if __name__ == "__main__":
    download_model()
