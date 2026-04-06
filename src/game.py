import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os
import random
import numpy as np

class GestureHeroGame:
    def __init__(self, model_path):
        # 1. Configuração da IA (MediaPipe)
        # Definimos o caminho do modelo e criamos o reconhecedor de gestos
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

        # 2. Configurações do Jogo
        # Lista de gestos que o MediaPipe reconhece por padrão
        self.gestures_pool = ['Open_Palm', 'Closed_Fist', 'Victory', 'Pointing_Up']
        
        # Mapeamento para exibição amigável em Português
        self.gestures_pt = {
            'Open_Palm': 'MAO ABERTA',
            'Closed_Fist': 'MAO FECHADA',
            'Victory': 'SINAL DE V',
            'Pointing_Up': 'DEDO P/ CIMA'
        }
        
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.current_command = None
        self.command_start_time = 0
        self.time_limit = 3.0 # Limite inicial de 3 segundos por gesto
        
        # 3. Elementos Visuais e Cores (Formato BGR para o OpenCV)
        self.feedback_text = "PREPARE-SE!"
        self.feedback_color = (0, 255, 255) # Ciano Neon
        self.theme_main = (255, 0, 255) # Magenta
        self.last_result_time = 0

    def get_new_command(self):
        """Sorteia um novo gesto e inicia o cronômetro"""
        self.current_command = random.choice(self.gestures_pool)
        self.command_start_time = time.time()
        self.feedback_text = f"{self.gestures_pt[self.current_command]}!"
        self.feedback_color = (0, 255, 255)

    def draw_text_with_shadow(self, img, text, pos, font, scale, color, thickness, shadow_color=(0, 0, 0)):
        """Desenha texto com um contorno/sombra para facilitar a leitura em qualquer fundo"""
        # Desenha a sombra (preta) com um pequeno deslocamento
        cv2.putText(img, text, (pos[0]+2, pos[1]+2), font, scale, shadow_color, thickness+1, cv2.LINE_AA)
        # Desenha o texto principal por cima
        cv2.putText(img, text, pos, font, scale, color, thickness, cv2.LINE_AA)

    def draw_user_lives(self, img, x, y, size, lives, color, shadow_color=(0, 0, 0)):
        """Desenha corações estilizados para representar as vidas do jogador"""
        for i in range(lives):
            base_x = x + i * (size * 5 + 10)
            offset = 2
            
            # Sombra do coração
            cv2.circle(img, (base_x - size + offset, y + offset), size, shadow_color, -1)
            cv2.circle(img, (base_x + size + offset, y + offset), size, shadow_color, -1)
            pts = np.array([[base_x - 2*size + offset, y + offset], 
                            [base_x + 2*size + offset, y + offset], 
                            [base_x + offset, y + 2*size + int(size*0.5) + offset]], np.int32)
            cv2.fillConvexPoly(img, pts, shadow_color)

            # Coração principal
            cv2.circle(img, (base_x - size, y), size, color, -1)
            cv2.circle(img, (base_x + size, y), size, color, -1)
            pts = np.array([[base_x - 2*size, y], 
                            [base_x + 2*size, y], 
                            [base_x, y + 2*size + int(size*0.5)]], np.int32)
            cv2.fillConvexPoly(img, pts, color)

    def process_frame(self, frame):
        """Processa cada frame da webcam para detectar gestos e atualizar a lógica do jogo"""
        if self.game_over:
            return self.draw_game_over(frame)

        # Converte o frame (OpenCV usa BGR) para o formato MediaPipe (RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = self.recognizer.recognize(mp_image)

        # Se não houver um comando ativo, sorteia um
        if self.current_command is None:
            self.get_new_command()

        # Calcula quanto tempo passou desde o início do comando atual
        elapsed_time = time.time() - self.command_start_time
        
        # Lógica de Tempo Esgotado (Timeout)
        if elapsed_time > self.time_limit:
            self.lives -= 1
            self.feedback_text = "MUITO LENTO!"
            self.feedback_color = (0, 0, 255) # Vermelho
            if self.lives <= 0:
                self.game_over = True
            else:
                self.get_new_command()

        # Lógica de Acerto (Sucesso)
        if result.gestures:
            detected_gesture = result.gestures[0][0].category_name
            # Se o gesto detectado for o comando que o jogo pediu
            if detected_gesture == self.current_command:
                self.score += 100
                self.feedback_text = "PERFEITO!"
                self.feedback_color = (0, 255, 0) # Verde
                self.get_new_command()
                # Aumenta a dificuldade diminuindo o tempo limite conforme o jogador acerta
                self.time_limit = max(1.2, self.time_limit * 0.97)

        return self.draw_hud(frame, elapsed_time)

    def draw_hud(self, frame, elapsed):
        """Desenha a interface do usuário (pontos, vidas, timer) na tela"""
        h, w, _ = frame.shape
        overlay = frame.copy()
        
        # 1. Barra Superior (Semi-transparente)
        cv2.rectangle(overlay, (0, 0), (w, 70), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Informações de Score e Título das Vidas
        self.draw_text_with_shadow(frame, f"PONTOS: {self.score}", (30, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        self.draw_text_with_shadow(frame, "VIDAS:", (w - 230, 45), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
        
        # Desenha os corações representando as vidas restantes
        heart_color = (0, 0, 255) if self.lives > 1 else (0, 165, 255)
        self.draw_user_lives(frame, w - 120, 37, 7, self.lives, heart_color)

        # 2. Painel Central de Instrução
        # Criamos um retângulo de foco no centro para destacar o gesto atual
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), (20, 20, 20), -1)
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), self.feedback_color, 2)
        
        # Desenha o comando ou feedback no centro, calculado para ficar alinhado
        text_cmd = self.feedback_text
        font_cmd = cv2.FONT_HERSHEY_DUPLEX
        scale_cmd = 1.3
        thick_cmd = 2
        size_cmd, _ = cv2.getTextSize(text_cmd, font_cmd, scale_cmd, thick_cmd)
        
        box_center_y = h // 2 - 85
        text_x = (w - size_cmd[0]) // 2
        text_y = box_center_y + (size_cmd[1] // 2)
        
        self.draw_text_with_shadow(frame, text_cmd, (text_x, text_y), font_cmd, scale_cmd, self.feedback_color, thick_cmd)

        # 3. Barra de Tempo Regressiva
        # Fundo da barra
        cv2.rectangle(frame, (50, h - 40), (w - 50, h - 20), (50, 50, 50), -1)
        # Progresso da barra (diminui conforme o tempo passa)
        progress = 1 - (elapsed / self.time_limit)
        bar_width = int((w - 100) * progress)
        # Transição de cor (Verde -> Amarelo -> Vermelho)
        bar_color = (0, int(255 * progress), int(255 * (1-progress))) 
        cv2.rectangle(frame, (50, h - 40), (50 + bar_width, h - 20), bar_color, -1)
        # Borda de acabamento
        cv2.rectangle(frame, (50, h - 40), (w - 50, h - 20), (200, 200, 200), 1)

        return frame

    def draw_game_over(self, frame):
        """Desenha a tela de fim de jogo com score final e efeitos visuais"""
        h, w, _ = frame.shape
        # Aplica um desfoque (blur) no fundo
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        
        # Camada escura transparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Título do Game Over
        text1 = "MISSÃO FALHOU"
        font1 = cv2.FONT_HERSHEY_DUPLEX
        scale1 = 2
        thick1 = 4
        size1, _ = cv2.getTextSize(text1, font1, scale1, thick1)
        self.draw_text_with_shadow(frame, text1, ((w - size1[0]) // 2, h // 2 - 50), font1, scale1, (0, 0, 255), thick1)

        # Pontuação Final
        text2 = f"PONTUACAO FINAL: {self.score}"
        font2 = cv2.FONT_HERSHEY_DUPLEX
        scale2 = 1
        thick2 = 2
        size2, _ = cv2.getTextSize(text2, font2, scale2, thick2)
        self.draw_text_with_shadow(frame, text2, ((w - size2[0]) // 2, h // 2 + 50), font2, scale2, (255, 255, 255), thick2)

        # Instruções de reinício
        text3 = "Pressione 'r' para Recomecar ou 'q' para Sair"
        font3 = cv2.FONT_HERSHEY_DUPLEX
        scale3 = 0.7
        thick3 = 1
        size3, _ = cv2.getTextSize(text3, font3, scale3, thick3)
        self.draw_text_with_shadow(frame, text3, ((w - size3[0]) // 2, h // 2 + 130), font3, scale3, (180, 180, 180), thick3)
        
        return frame

def run_game():
    """Função principal que inicia a webcam e gerência o loop do jogo"""
    # Define o caminho do arquivo de IA (.task)
    model_path = os.path.join("models", "gesture_recognizer.task")
    
    # Instancia o objeto do jogo
    game = GestureHeroGame(model_path)
    
    # Inicia a captura da webcam padrão (índice 0)
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Espelha o frame horizontalmente para a visão do usuário ficar intuitiva
        frame = cv2.flip(frame, 1)
        
        # Envia o frame capturado para ser processado pela IA e lógica do jogo
        frame = game.process_frame(frame)

        # Abre a janela do jogo
        cv2.imshow('Gesture Hero v2.1 - Edicao Premium', frame)

        # Verifica teclas pressionadas
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # Sair
            break
        elif key == ord('r') and game.game_over: # Reiniciar no Game Over
            game = GestureHeroGame(model_path)

    # Libera os recursos da câmera e fecha as janelas
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
