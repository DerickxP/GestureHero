import cv2
import mediapipe as mp
import numpy as np
import os
import time

GESTURES = ['open_hand', 'closed_fist', 'point_left', 'point_right']
DATA_PATH = os.path.join('..', 'data')
SAMPLES_PER_GESTURE = 200

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

def collect_data():
    cap = cv2.VideoCapture(0)
    
    for gesture in GESTURES:
        gesture_dir = os.path.join(DATA_PATH, gesture)
        os.makedirs(gesture_dir, exist_ok=True)
        
        print(f"\n--- Preparado para o gesto: {gesture} ---")
        print("Posicione sua mão na frente da câmera. Começaremos em 3 segundos...")
        time.sleep(3)
        
        count = 0
        while count < SAMPLES_PER_GESTURE:
            ret, frame = cap.read()
            if not ret: break
            
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])
                    
                    file_path = os.path.join(gesture_dir, f"{count}.npy")
                    np.save(file_path, landmarks)
                    count += 1
            
            cv2.putText(frame, f"Gesto: {gesture} | Amostras: {count}/{SAMPLES_PER_GESTURE}", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Coleta de Dados - Gesture Hero", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()
    print("\nColeta concluída com sucesso!")

if __name__ == "__main__":
    collect_data()
