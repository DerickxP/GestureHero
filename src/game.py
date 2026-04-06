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
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.current_command = None
        self.command_start_time = 0
        self.time_limit = 3.0
        
        # 3. Visuals & Themes
        self.feedback_text = "READY?"
        self.feedback_color = (0, 255, 255) # Cyan Neon
        self.theme_main = (255, 0, 255) # Magenta
        self.last_result_time = 0

    def get_new_command(self):
        self.current_command = random.choice(self.gestures_pool)
        self.command_start_time = time.time()
        self.feedback_text = f"{self.current_command}!"
        self.feedback_color = (0, 255, 255)

    def draw_text_with_shadow(self, img, text, pos, font, scale, color, thickness, shadow_color=(0, 0, 0)):
        # Draw Shadow/Outline
        cv2.putText(img, text, (pos[0]+2, pos[1]+2), font, scale, shadow_color, thickness+1, cv2.LINE_AA)
        # Draw Main Text
        cv2.putText(img, text, pos, font, scale, color, thickness, cv2.LINE_AA)

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
            self.feedback_text = "TOO SLOW!"
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
                self.feedback_text = "PERFECT!"
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
        self.draw_text_with_shadow(frame, f"SCORE: {self.score}", (30, 45), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 2)
        
        # Hearts for Lives
        heart_color = (0, 0, 255) if self.lives > 1 else (0, 165, 255)
        self.draw_text_with_shadow(frame, f"LIVES: {'L' * self.lives}", (w - 280, 45), cv2.FONT_HERSHEY_DUPLEX, 0.9, heart_color, 2)

        # 2. Central Instruction Panel
        # Create a darker focus area in the middle for the command
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), (20, 20, 20), -1)
        cv2.rectangle(frame, (w//2 - 200, h//2 - 130), (w//2 + 200, h//2 - 40), self.feedback_color, 2)
        
        # Draw central command
        self.draw_text_with_shadow(frame, self.feedback_text, (w//2 - 160, h//2 - 70), cv2.FONT_HERSHEY_DUPLEX, 1.3, self.feedback_color, 2)

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

        self.draw_text_with_shadow(frame, "MISSION FAILED", (w//2 - 200, h//2 - 50), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 4)
        self.draw_text_with_shadow(frame, f"FINAL SCORE: {self.score}", (w//2 - 140, h//2 + 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
        self.draw_text_with_shadow(frame, "Press 'r' to Retry or 'q' to Quit", (w//2 - 220, h//2 + 130), cv2.FONT_HERSHEY_DUPLEX, 0.7, (180, 180, 180), 1)
        
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
