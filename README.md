[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/BOO70ufO)

# 5.1 Exploring Hyperparameters
Erklärung zum Vorgehen befindet sich am Anfang des Notebooks "hyperparameters.ipynb". Zugehörige Grafiken finden sich in den jeweiligen Ordnern. Ich habe sowohl die Metriken der einzelnen Parameter dargestellt als auch Grafiken zum Vergleich zwischen den Parametern. Alles weitere siehe eben Notebook.

# 5.2 Gathering a Dataset
Trainiert wurde das Modell auf alle 5 Gesten, allerdings kommt "no_gesture" ja auch immer mit. Das verwendete Modell hat also 6 mögliche Outputs und ist als "gesture_recognition-keras" in 02-dataset gespeichert. Es scheint alles gut zu predicten, aber bei der Confusion Matrix hat sich ein Fehler eingeschlichen. Da die Label Indizes und Namen kein "no_gesture" enthalten, weil meine Testbilder nur Hände mit Gesten enthalten, kommt ab index 2 die Zuordnung durcheinander und er glaubt es falsch zu predicten. Das erklärt, warum ab Zeile 2 die Matrix um 1 nach unten verschoben gehört!

# 5.3 Gesture-based Media Controls