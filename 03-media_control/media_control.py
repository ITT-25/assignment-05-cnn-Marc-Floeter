import cv2
import numpy as np
from pynput.keyboard import Controller, Key
import keras.models
import time


# EINSTELLUNGEN ############################################################################

# Model
PREDICTION_MODEL_PATH = "gesture_recognition.keras"
LABEL_NAMES = ['like', 'no_gesture', 'dislike', 'stop', 'rock', 'peace']
IMG_SIZE = 64
SIZE = (IMG_SIZE, IMG_SIZE)
COLOR_CHANNELS = 3

# Auslösecooldown
PLAY_PAUSE_COOLDOWN = 1.5
VOLUME_COOLDOWN = 0.2 

# Erkennungsstrategie
RECOGNITION_WINDOW_ON = True
RECOGNITION_WINDOW_SIZE = 200
RECOGNITION_WINDOW_POS = 100

# Anzeigeoptionen
INPUT_WINDOW_ON = True
RECOGNITION_WINDOW_COLOR = (0, 255, 0)
PREDICTION_TEXT_ON = True
PREDICTION_TEXT_POS = (50, 50)
TEXT_COLOR = (0, 0, 0)

KEYBOARD = Controller()


# VARIABLEN ################################################################################

model = keras.models.load_model(PREDICTION_MODEL_PATH)
last_prediction = None
last_action_time = time.time()


# PREPROCESSING DES KAMERAFRAMES ###########################################################
def preprocess(frame):

    if COLOR_CHANNELS == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if RECOGNITION_WINDOW_ON:
        frame = frame[RECOGNITION_WINDOW_POS : RECOGNITION_WINDOW_POS + RECOGNITION_WINDOW_SIZE, RECOGNITION_WINDOW_POS : RECOGNITION_WINDOW_POS + RECOGNITION_WINDOW_SIZE] # Gestenerkennung auf festen Bereich begrenzen

    resized_frame = cv2.resize(frame, SIZE)  # Anpassung an Trainingsformat des Modells
    normalized_frame = np.array(resized_frame).astype('float32')
    normalized_frame = normalized_frame / 255.0
    reshaped_frame = normalized_frame.reshape(1, IMG_SIZE, IMG_SIZE, COLOR_CHANNELS)

    return reshaped_frame


# BUTTON / MEDIA CONTROL MAPPING ###########################################################
def trigger_media_control(label):
    global last_prediction, last_action_time

    time_since_last_action = time.time() - last_action_time

    # Verhindere wiederholte Eingaben zu schnell
    if label == last_prediction:
        if label == "stop" and time_since_last_action < PLAY_PAUSE_COOLDOWN:
            return
        elif (label == "like" or label == "dislike") and time_since_last_action < VOLUME_COOLDOWN:
            return
    
    print(label)
    
    if label == "stop":
        print("Pause / Play")
        KEYBOARD.press(Key.media_play_pause)
        KEYBOARD.release(Key.media_play_pause)

    elif label == "like":
        print("Lauter")
        KEYBOARD.press(Key.media_volume_up)
        KEYBOARD.release(Key.media_volume_up)

    elif label == "dislike":
        print("Leiser")
        KEYBOARD.press(Key.media_volume_down)
        KEYBOARD.release(Key.media_volume_down)
    
    else: 
        return

    last_prediction = label
    last_action_time = time.time()


# KAMERA LOOP ##############################################################################

# Kameralinse öffnen
cap = cv2.VideoCapture(0)

try:
    while True:

        # Kameraframe auslesen
        ret, frame = cap.read()
        if not ret:
            print("Kamerabild nicht erkannt")
            break
        
        # Preprocessing des Frames
        preprocessed_frame = preprocess(frame)

        # Prediction der Geste durch Model
        prediction = model.predict(preprocessed_frame, verbose=0)
        predicted_gesture = LABEL_NAMES[np.argmax(prediction)]

        # Auslösen der Media Controls durch Prediction
        trigger_media_control(predicted_gesture)

        # Fenster zur Eingabe
        if INPUT_WINDOW_ON:

            if RECOGNITION_WINDOW_ON:
                cv2.rectangle(frame, (RECOGNITION_WINDOW_POS, RECOGNITION_WINDOW_POS), (RECOGNITION_WINDOW_POS + RECOGNITION_WINDOW_SIZE, RECOGNITION_WINDOW_POS + RECOGNITION_WINDOW_SIZE), RECOGNITION_WINDOW_COLOR, 2)
            
            if PREDICTION_TEXT_ON:
                cv2.putText(frame, predicted_gesture, PREDICTION_TEXT_POS, cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)
            
            cv2.imshow("Gestensteuerung", frame)

        # Prüfen, ob Fenster mit X geschlossen wurde
        if cv2.getWindowProperty("Gestensteuerung", cv2.WND_PROP_VISIBLE) < 1:
            print("Fenster geschlossen – Programm beendet")
            break

        # Beenden mit q
        if cv2.waitKey(1) == ord('q'):
            break

except KeyboardInterrupt:
    print("Programm beendet")

finally:
    cap.release()
    cv2.destroyAllWindows()
