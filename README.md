[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/BOO70ufO)

# 5.1 Exploring Hyperparameters
Erklärung zum Vorgehen befindet sich am Anfang des Notebooks "hyperparameters.ipynb". Zugehörige Grafiken finden sich in den jeweiligen Ordnern. Ich habe sowohl die Metriken der einzelnen Parameter dargestellt als auch Grafiken zum Vergleich zwischen den Parametern. Alles weitere siehe eben Notebook.

# 5.2 Gathering a Dataset
Trainiert wurde das Modell auf alle 5 Gesten, allerdings kommt "no_gesture" ja auch immer mit. Das verwendete Modell hat also 6 mögliche Outputs und ist als "gesture_recognition-keras" in 02-dataset gespeichert. Es scheint alles gut zu predicten, aber bei der Confusion Matrix hat sich ein Fehler eingeschlichen. Da die Label Indizes und Namen kein "no_gesture" enthalten, weil meine Testbilder nur Hände mit Gesten enthalten, kommt ab index 2 die Zuordnung durcheinander und er glaubt es falsch zu predicten. Das erklärt, warum ab Zeile 2 die Matrix um 1 nach unten verschoben gehört!

# 5.3 Gesture-based Media Controls
## Kurzbeschreibung
Programm erkennt Handgesten und mappt sie auf Media-Control-Tasten:
1. Stop = Pause / Play (on/off)
2. Like = Lauter (kontinuierlich)
3. Dislike = Leiser (kontinuierlich)

## Setup und Bedienung
1. Navigiere in den Ordner "03-media_control"
<<<<<<< HEAD
2. Erstelle venv mit "python -m venv venv" und aktiviere es mit venv\scripts\activate
=======
2. Aktiviere venv mit venv\scripts\activate
>>>>>>> aba59ca (Assignment 5.3: Gestensteuerung für Media Controlls funktioniert (aber nur mit Recognition Window und einigen "false alarms", Erkennung der Art der Geste, wenn eine da ist, klappt gut))
3. Installiere Abhängigkeiten aus "requirements.txt"
4. Starte Anwendung mit "python media_control.py"
5. Öffne ggf. Input-Fenster
6. Halte Handgeste (ggf. innerhalb des Recognitio-Windows) -> KONTROLLIERE DIE MEDIEN

## Einstellungen
- Pfad zum zu verwendenden Modell samt erkennbarer Gesten, Bildgröße und Farbkanälen
- Auslösecooldown (wie lange eine on / off Geste gehalten werden muss, damit sich ihr Effekt wiederholt)
- Optionales Recognition-Window, um den Bereich, in dem die Geste erkannt werden soll, zu definieren
- Optionale Anzeige des Kamerabildes, um die Geste richtig am Recognition-Window auszurichten und ggf. Feedback zum Label der erkannten Geste zu erhalten