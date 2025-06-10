import cv2
import os
import json
import uuid
from tkinter import Tk, Canvas, StringVar, OptionMenu, Button
from PIL import Image, ImageTk

# Konfiguration
NAME = 'marc'
GESTURES = ['like', 'dislike', 'stop', 'rock', 'peace']
HEIGHT = 1080
WIDTH = 1920
FILETYPE = "jpg"

DISPLAY_WIDTH = 960
DISPLAY_HEIGHT = 540

BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "marc_dataset")
ANNOTATION_FILE = os.path.join(SAVE_DIR, f"annot-{NAME}.json")

# Globals
start_x = 0
start_y = 0
end_x = 0
end_y = 0
current_img = None
rect_id = None
annotations = {}

os.makedirs(SAVE_DIR, exist_ok=True)

if os.path.exists(ANNOTATION_FILE):
    try:
        with open(ANNOTATION_FILE, "r") as f:
            annotations = json.load(f)
    except json.JSONDecodeError:
        print(f"Warnung: '{ANNOTATION_FILE}' ist leer oder ungültig. Starte mit leerem Dictionary.")
        annotations = {}
else:
    annotations = {}

def annotate_image(image_np):
    global start_x, start_y, end_x, end_y, current_img, rect_id

    # PIL Image vorbereiten
    current_img = Image.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    orig_width, orig_height = current_img.size

    # Skalierung für Anzeige
    max_display_width = DISPLAY_WIDTH
    max_display_height = DISPLAY_HEIGHT
    scale = min(max_display_width / orig_width, max_display_height / orig_height, 1)
    disp_width = int(orig_width * scale)
    disp_height = int(orig_height * scale)

    # Tkinter Setup
    root = Tk()
    root.title("Annotation Tool")

    resized_img = current_img.resize((disp_width, disp_height), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(resized_img)

    canvas = Canvas(root, width=disp_width, height=disp_height)
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.pack()

    label_var = StringVar(root)
    label_var.set(GESTURES[0])

    label_menu = OptionMenu(root, label_var, *GESTURES, "no-gesture")
    label_menu.pack()

    def on_mouse_down(event):
        global start_x, start_y
        start_x, start_y = event.x, event.y

    def on_mouse_up(event):
        global end_x, end_y, rect_id
        end_x, end_y = event.x, event.y
        if rect_id:
            canvas.delete(rect_id)
        rect_id = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red", width=2)

    def save_annotation():
        global start_x, start_y, end_x, end_y

        # Koordinaten bereinigen und normalisieren
        xmin = min(start_x, end_x) / scale / orig_width
        ymin = min(start_y, end_y) / scale / orig_height
        xmax = max(start_x, end_x) / scale / orig_width
        ymax = max(start_y, end_y) / scale / orig_height
        bbox = [xmin, ymin, xmax - xmin, ymax - ymin]

        bbox_rounded = [round(coord, 8) for coord in bbox]

        label = label_var.get()

        # Verzeichnis + Dateiname
        gesture_dir = os.path.join(SAVE_DIR, label)
        os.makedirs(gesture_dir, exist_ok=True)

        image_id = str(uuid.uuid4())
        filename = f"{image_id}.{FILETYPE}"
        filepath = os.path.join(gesture_dir, filename)

        # Bild speichern
        current_img.save(filepath)

        # Annotation im HaGRID-Format
        annotations[image_id] = {
            "bboxes": [bbox_rounded],
            "labels": [label],
            "landmarks": [[]],
            "leading_conf": 1.0,
            "leading_hand": "right",
            "user_id": "flm05277"
        }

        with open(ANNOTATION_FILE, "w") as f:
            json.dump(annotations, f, indent=2)

        print(f"Bild und Annotation gespeichert: {filepath}")
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    Button(root, text="Speichern", command=save_annotation).pack()
    root.mainloop()


# -------- Webcam Aufnahme --------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamerafehler.")
        break

    # Frame fürs Anzeigen skalieren
    frame_display = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

    cv2.imshow("Aufnahme - 's' annotieren, 'q' beenden", frame_display)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        annotate_image(frame)  # Original Frame an annotate_image übergeben

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
