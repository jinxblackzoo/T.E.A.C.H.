# Hauptskript zum Starten der T.E.A.C.H.-Anwendung und Initialisierung der Qt-Applikation
import sys  # Systemmodul für Kommandozeilenargumente und Programmbeendigung
from PySide6.QtWidgets import QApplication  # Import der Qt-Anwendungsklasse
from core.app import TEACH  # Import der Hauptfensterklasse aus dem Core-Package
from modules.klar_module import register as register_klar  # Modul-Registrierung

def main():  # Startet die T.E.A.C.H.-Anwendung
    app = QApplication(sys.argv)  # Erzeuge Qt-Anwendung mit Kommandozeilenargumenten
    window = TEACH()  # Initialisiere das Hauptfenster der Anwendung
    register_klar(window)  # KLAR-Modul bei TEACH anmelden
    window.show()  # Zeige das Hauptfenster an
    sys.exit(app.exec())  # Starte die Qt-Ereignisschleife und beende das Programm

if __name__ == "__main__":  # Nur bei direkter Ausführung
    main()  # Aufruf der main()-Funktion
