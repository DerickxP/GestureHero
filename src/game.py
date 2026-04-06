import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import os

# 1. Configuration: Model Path and Recognizer Setup
model_path = os.path.join("models", "gesture_recognizer.task")

# Base options and Task options initialization
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

def run_game():
    # Initialize webcam capture (index 0)
    cap = cv2.VideoCapture(0)
    
    print("Starting Gesture Hero with Google AI Recognition...")
    print("Press 'q' to exit.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB (required by MediaPipe)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform real-time gesture recognition
        gesture_recognition_result = recognizer.recognize(mp_image)

        # HUD Logic: Display detection results if any
        if gesture_recognition_result.gestures:
            top_gesture = gesture_recognition_result.gestures[0][0].category_name
            confidence = gesture_recognition_result.gestures[0][0].score
            
            # Draw Gesture information and Confidence on screen
            cv2.putText(frame, f"Gesture: {top_gesture} ({confidence:.2f})", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # Fallback message when no hand is detected
            cv2.putText(frame, "No gesture detected", 
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the output window
        cv2.imshow('Gesture Hero - Recognition Test', frame)

        # Key listener for closing the app
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_game()
