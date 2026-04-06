import urllib.request
import os

def download_model():
    # Official MediaPipe model URL
    model_url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
    save_path = os.path.join("models", "gesture_recognizer.task")

    # Ensure the 'models' directory exists
    os.makedirs("models", exist_ok=True)

    print(f"Starting model download to: {save_path}...")
    try:
        # Download the file using urllib
        urllib.request.urlretrieve(model_url, save_path)
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading the model: {e}")

if __name__ == "__main__":
    download_model()
