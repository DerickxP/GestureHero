import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os

# 1. Configuração do Modelo e Reconhecedor
model_path = os.path.join("models", "gesture_recognizer.task")

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

def run_game():
    cap = cv2.VideoCapture(0)
    
    print("Iniciando Gesture Hero com Reconhecimento do Google...")
    print("Pressione 'q' para sair.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Inverter horizontalmente para efeito de espelho
        frame = cv2.flip(frame, 1)

        # Converter BGR para RGB para o MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Realizar o reconhecimento do gesto
        gesture_recognition_result = recognizer.recognize(mp_image)

        # Exibir o resultado se houver gestos detectados
        if gesture_recognition_result.gestures:
            top_gesture = gesture_recognition_result.gestures[0][0].category_name
            confidence = gesture_recognition_result.gestures[0][0].score
            
            # HUD simples
            cv2.putText(frame, f"Gesto: {top_gesture} ({confidence:.2f})", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Nenhum gesto detectado", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Mostrar o frame
        cv2.imshow('Gesture Hero - Teste de Reconhecimento', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
