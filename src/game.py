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
        # 1. AI Setup
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

        # 2. Game Settings
        self.gestures_pool = ['Open_Palm', 'Closed_Fist', 'Victory', 'Pointing_Up']
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
        self.time_limit = 3.0
        
        # 3. Visuals & Themes
        self.feedback_text = "PREPARE-SE!"
        self.feedback_color = (0, 255, 255) # Cyan Neon
        self.theme_main = (255, 0, 255) # Magenta
        self.last_result_time = 0

    def get_new_command(self):
        self.current_command = random.choice(self.gestures_pool)
        self.command_start_time = time.time()
        self.feedback_text = f"{self.gestures_pt[self.current_command]}!"
        self.feedback_color = (0, 255, 255)

    def draw_text_with_shadow(self, img, text, pos, font, scale, color, thickness, shadow_color=(0, 0, 0)):
        # Draw Shadow/Outline
        cv2.putText(img, text, (pos[0]+2, pos[1]+2), font, scale, shadow_color, thickness+1, cv2.LINE_AA)
        # Draw Main Text
        cv2.putText(img, text, pos, font, scale, color, thickness, cv2.LINE_AA)

    def draw_user_lives(self, img, x, y, size, lives, color, shadow_color=(0, 0, 0)):
        for i in range(lives):
            base_x = x + i * (size * 5 + 10)
            offset = 2
            
            # Shadow
            cv2.circle(img, (base_x - size + offset, y + offset), size, shadow_color, -1)
            cv2.circle(img, (base_x + size + offset, y + offset), size, shadow_color, -1)
            pts = np.array([[base_x - 2*size + offset, y + offset], 
                            [base_x + 2*size + offset, y + offset], 
                            [base_x + offset, y + 2*size + int(size*0.5) + offset]], np.int32)
            cv2.fillConvexPoly(img, pts, shadow_color)

            # Heart
            cv2.circle(img, (base_x - size, y), size, color, -1)
            cv2.circle(img, (base_x + size, y), size, color, -1)
            pts = np.array([[base_x - 2*size, y], 
                            [base_x + 2*size, y], 
                            [base_x, y + 2*size + int(size*0.5)]], np.int32)
            cv2.fillConvexPoly(img, pts, color)

    def process_frame(self, frame):
        if self.game_over:
            return self.draw_game_over(frame)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = self.recognizer.recognize(mp_image)

        if self.current_command is None:
            self.get_new_command()

        elapsed_time = time.time() - self.command_start_time
        
        # Timeout logic
        if elapsed_time > self.time_limit:
            self.lives -= 1
            self.feedback_text = "MUITO LENTO!"
            self.feedback_color = (0, 0, 255) 
            if self.lives <= 0:
                self.game_over = True
            else:
                self.get_new_command()

        # Success logic
        if result.gestures:
            detected_gesture = result.gestures[0][0].category_name
            if detected_gesture == self.current_command:
                self.score += 100
                self.feedback_text = "PERFEITO!"
                self.feedback_color = (0, 255, 0)
                self.get_new_command()
                self.time_limit = max(1.2, self.time_limit * 0.97)

        return self.draw_hud(frame, elapsed_time)

    def draw_hud(self, frame, elapsed):
        h, w, _ = frame.shape
        overlay = frame.copy()
        
        # 1. Top HUD Bar (Semi-transparent)
        cv2.rectangle(overlay, (0, 0), (w, 70), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        # Labels
        self.draw_text_with_shadow(frame, f"PONTOS: {self.score}", (30, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        self.draw_text_with_shadow(frame, "VIDAS:", (w - 230, 45), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
        
        # Hearts for Lives
        heart_color = (0, 0, 255) if self.lives > 1 else (0, 165, 255)
        self.draw_user_lives(frame, w - 120, 37, 7, self.lives, heart_color)

        # 2. Central Instruction Panel
        # Create a darker focus area in the middle for the command
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), (20, 20, 20), -1)
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), self.feedback_color, 2)
        
        # Draw central command (Centered dynamically)
        text_cmd = self.feedback_text
        font_cmd = cv2.FONT_HERSHEY_DUPLEX
        scale_cmd = 1.3
        thick_cmd = 2
        size_cmd, _ = cv2.getTextSize(text_cmd, font_cmd, scale_cmd, thick_cmd)
        
        # Center horizontally, and perfectly center vertically inside the rect (height range -130 to -40)
        box_center_y = h // 2 - 85
        text_x = (w - size_cmd[0]) // 2
        text_y = box_center_y + (size_cmd[1] // 2)
        
        self.draw_text_with_shadow(frame, text_cmd, (text_x, text_y), font_cmd, scale_cmd, self.feedback_color, thick_cmd)

        # 3. Premium Timer Bar
        # Bar background
        cv2.rectangle(frame, (50, h - 40), (w - 50, h - 20), (50, 50, 50), -1)
        # Bar progress
        progress = 1 - (elapsed / self.time_limit)
        bar_width = int((w - 100) * progress)
        bar_color = (0, int(255 * progress), int(255 * (1-progress))) # Transitions Green -> Yellow -> Red
        cv2.rectangle(frame, (50, h - 40), (50 + bar_width, h - 20), bar_color, -1)
        # Border
        cv2.rectangle(frame, (50, h - 40), (w - 50, h - 20), (200, 200, 200), 1)

        return frame

    def draw_game_over(self, frame):
        h, w, _ = frame.shape
        # Blur the background for the Game Over effect
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        
        # Dark overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Draw "MISSION FAILED"
        text1 = "MISSION FAILED"
        font1 = cv2.FONT_HERSHEY_DUPLEX
        scale1 = 2
        thick1 = 4
        size1, _ = cv2.getTextSize(text1, font1, scale1, thick1)
        self.draw_text_with_shadow(frame, text1, ((w - size1[0]) // 2, h // 2 - 50), font1, scale1, (0, 0, 255), thick1)

        # Draw "FINAL SCORE"
        text2 = f"FINAL SCORE: {self.score}"
        font2 = cv2.FONT_HERSHEY_DUPLEX
        scale2 = 1
        thick2 = 2
        size2, _ = cv2.getTextSize(text2, font2, scale2, thick2)
        self.draw_text_with_shadow(frame, text2, ((w - size2[0]) // 2, h // 2 + 50), font2, scale2, (255, 255, 255), thick2)

        # Draw instructions
        text3 = "Press 'r' to Retry or 'q' to Quit"
        font3 = cv2.FONT_HERSHEY_DUPLEX
        scale3 = 0.7
        thick3 = 1
        size3, _ = cv2.getTextSize(text3, font3, scale3, thick3)
        self.draw_text_with_shadow(frame, text3, ((w - size3[0]) // 2, h // 2 + 130), font3, scale3, (180, 180, 180), thick3)
        
        return frame

def run_game():
    model_path = os.path.join("models", "gesture_recognizer.task")
    game = GestureHeroGame(model_path)
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        frame = game.process_frame(frame)

        cv2.imshow('Gesture Hero v2.1 - Premium Edition', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and game.game_over:
            game = GestureHeroGame(model_path)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
