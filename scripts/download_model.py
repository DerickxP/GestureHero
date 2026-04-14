import urllib.request
import os

def download_model():
    model_url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
    save_path = os.path.join("models", "gesture_recognizer.task")

    os.makedirs("models", exist_ok=True)

    print(f"Starting model download to: {save_path}...")
    try:
        urllib.request.urlretrieve(model_url, save_path)
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading the model: {e}")

if __name__ == "__main__":
    download_model()
