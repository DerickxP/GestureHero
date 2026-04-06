import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os
import random

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
        self.time_limit = 3.0  # Seconds per gesture (Dynamic difficulty later)
        
        # 3. Visuals
        self.feedback_text = "READY?"
        self.feedback_color = (255, 255, 255) # White
        self.last_result_time = 0

    def get_new_command(self):
        self.current_command = random.choice(self.gestures_pool)
        self.command_start_time = time.time()
        self.feedback_text = f"DO: {self.current_command}!"
        self.feedback_color = (255, 255, 255)

    def process_frame(self, frame):
        if self.game_over:
            return self.draw_game_over(frame)

        # Convert to MediaPipe format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = self.recognizer.recognize(mp_image)

        # Initial command
        if self.current_command is None:
            self.get_new_command()

        # Check for timeout
        elapsed_time = time.time() - self.command_start_time
        if elapsed_time > self.time_limit:
            self.lives -= 1
            self.feedback_text = "MISS! -1 LIFE"
            self.feedback_color = (0, 0, 255) # Red
            self.last_result_time = time.time()
            if self.lives <= 0:
                self.game_over = True
            else:
                self.get_new_command()

        # Check for success
        if result.gestures:
            detected_gesture = result.gestures[0][0].category_name
            if detected_gesture == self.current_command:
                self.score += 100
                self.feedback_text = "PERFECT! +100"
                self.feedback_color = (0, 255, 0) # Green
                self.get_new_command()
                # Increase difficulty slightly
                self.time_limit = max(1.5, self.time_limit * 0.98)

        return self.draw_hud(frame, elapsed_time)

    def draw_hud(self, frame, elapsed):
        h, w, _ = frame.shape
        
        # 1. Top Bar: Score and Lives
        cv2.rectangle(frame, (0, 0), (w, 60), (0, 0, 0), -1)
        cv2.putText(frame, f"SCORE: {self.score}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f"LIVES: {' <3 ' * self.lives}", (w - 250, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 2. Central Command/Feedback
        cv2.putText(frame, self.feedback_text, (w//2 - 150, h//2 - 100), cv2.FONT_HERSHEY_DUPLEX, 1.5, self.feedback_color, 3)

        # 3. Timer Bar
        timer_width = int(w * (1 - (elapsed / self.time_limit)))
        cv2.rectangle(frame, (0, h - 20), (timer_width, h), (0, 255, 255), -1)

        return frame

    def draw_game_over(self, frame):
        h, w, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.putText(frame, "GAME OVER", (w//2 - 150, h//2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.putText(frame, f"FINAL SCORE: {self.score}", (w//2 - 150, h//2 + 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'r' to Restart or 'q' to Quit", (w//2 - 200, h//2 + 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
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

        cv2.imshow('Gesture Hero v2.0 - Gaming Experience', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and game.game_over:
            game = GestureHeroGame(model_path) # Restart

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
