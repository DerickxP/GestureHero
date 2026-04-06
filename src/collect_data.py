import cv2  # OpenCV: Usado para capturar vídeo e desenhar na tela
import mediapipe as mp  # MediaPipe: A IA do Google que detecta as mãos
import numpy as np  # NumPy: Biblioteca para lidar com números e matrizes
import os  # OS: Permite manipular pastas e arquivos do Windows
import time  # Time: Gera as pausas de 3 segundos entre os gestos

# 1. Configurações Iniciais: Definimos os nomes e onde salvar tudo
GESTURES = ['open_hand', 'closed_fist', 'point_left', 'point_right']
DATA_PATH = 'data'  # Pasta onde os gestos serão salvos
SAMPLES_PER_GESTURE = 200  # Quantidade de 'fotos' numéricas para cada gesto

# 2. Inicializar o 'Cérebro' do MediaPipe
mp_hands = mp.solutions.hands  # Acessa a ferramenta de mãos
mp_draw = mp.solutions.drawing_utils  # Ferramenta para desenhar as linhas verdes
hands = mp_hands.Hands(
    static_image_mode=False,  # Falso porque estamos usando vídeo em tempo real
    max_num_hands=1,  # Foca em apenas uma mão para simplificar o jogo
    min_detection_confidence=0.7,  # Só aceita a mão se tiver 70% de certeza
    min_tracking_confidence=0.5  # Confiança mínima para continuar seguindo a mão
)

def collect_data():
    cap = cv2.VideoCapture(0)  # Liga a sua webcam padrão (índice 0)
    
    for gesture in GESTURES:
        # Cria a pasta do gesto (ex: data/open_hand) se ela ainda não existir
        gesture_dir = os.path.join(DATA_PATH, gesture)
        os.makedirs(gesture_dir, exist_ok=True)
        
        print(f"\n--- Preparado para o gesto: {gesture} ---")
        print("Posicione sua mão na frente da câmera. Começaremos em 3 segundos...")
        time.sleep(3)  # Pausa dramática para se posicionar
        
        count = 0
        while count < SAMPLES_PER_GESTURE:
            ret, frame = cap.read()  # Captura o frame atual da câmera
            if not ret: break
            
            # O MediaPipe precisa da imagem em RGB, mas o OpenCV usa BGR
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)  # A IA processa o frame e procura a mão
            
            # Se a IA encontrar a mão, vamos extrair os 21 pontos (landmarks)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Desenha as linhas e pontos verdes na tela para você ver
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Extraímos X, Y e Z de cada um dos 21 pontos (63 números no total)
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])
                    
                    # Salvamos esses 63 números num arquivo binário .npy (muito rápido)
                    file_path = os.path.join(gesture_dir, f"{count}.npy")
                    np.save(file_path, landmarks)
                    count += 1
            
            # Escreve textos na tela (HUD) para orientar o jogador
            cv2.putText(frame, f"Gesto: {gesture} | Amostras: {count}/{SAMPLES_PER_GESTURE}", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Coleta de Dados - Gesture Hero", frame)  # Abre a janela
            
            # Se você apertar a tecla 'q', a coleta para imediatamente
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    # Ao encerrar, desliga a câmera e fecha todas as janelas do Windows
    cap.release()
    cv2.destroyAllWindows()
    print("\nColeta concluída com sucesso!")

if __name__ == "__main__":
    collect_data()
