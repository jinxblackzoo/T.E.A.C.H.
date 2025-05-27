# Datei: src/core/app.py – Hauptanwendung mit Tab-basierter Navigation
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QTabWidget  # Import grundlegender Qt-Widgets
from PySide6.QtCore import Qt  # Import Qt-Kernfunktionen für Ausrichtung und Signale
from .module import TEACHModule  # Import der Basisklasse für Module

class TEACH(QMainWindow):  # Definition der Hauptfensterklasse, erbt von QMainWindow
    """Hauptfenster der T.E.A.C.H. Anwendung mit Tab-Navigation."""
    def __init__(self):  # Konstruktor: Einrichtung des Fensters und der UI-Komponenten
        super().__init__()  # Aufruf des Elternkonstruktors
        self.setWindowTitle("T.E.A.C.H. - Toll Ein Anderes Chaotisches Hilfeprogramm")  # Fenstertitel setzen
        self.setGeometry(100, 100, 1024, 768)  # Position und Größe des Fensters definieren

        # Zentrales Widget und Layout anlegen
        self.central_widget = QWidget()  # Hauptcontainer-Widget
        self.setCentralWidget(self.central_widget)  # Setzen als Zentral-Widget des Hauptfensters
        self.layout = QVBoxLayout(self.central_widget)  # Vertikales Layout für das Zentral-Widget

        # Tab-Widget für die Hauptnavigation erstellen
        self.tabs = QTabWidget()  # Tab-Container erzeugen
        self.tabs.addTab(SettingsMenu(), "Einstellungen")  # Tab für Einstellungen hinzufügen
        self.tabs.addTab(ReportingMenu(), "Berichte")  # Tab für Berichte hinzufügen
        self.tabs.addTab(ModuleMenu(), "Module")  # Tab für Modulverwaltung hinzufügen
        self.layout.addWidget(self.tabs)  # Tab-Container in das Hauptlayout einfügen

        # Begrüßungstext anzeigen
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")  # QLabel für Willkommensnachricht
        welcome_label.setAlignment(Qt.AlignCenter)  # Zentrieren des Textes
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")  # Stil anpassen
        self.layout.addWidget(welcome_label)  # Begrüßung in das Layout einfügen

        # Statusanzeige für Modul-Ladevorgang
        self.status_label = QLabel("Lade Module...")  # QLabel für Statusinformationen
        self.status_label.setAlignment(Qt.AlignCenter)  # Zentrierte Ausrichtung
        self.layout.addWidget(self.status_label)  # Status-Label in das Layout einfügen

        # Initialisierung der Modul-Struktur
        self.modules = {}  # Dictionary zum Speichern geladener Module
        self.load_modules()  # Aufruf der Methode zum Laden der Module

    def load_modules(self):  # Definition der Methode zum dynamischen Laden von Modulen
        """Lädt die verfügbaren Module dynamisch und aktualisiert die Statusanzeige."""
        self.status_label.setText("Module geladen: Noch keine Module implementiert")  # Status aktualisieren
        # Platzhalter: Logik zum automatischen Laden der Module hier implementieren

    def activate_module(self, module_name):  # Methode zum Aktivieren eines Moduls nach Namen
        """Aktiviert ein Modul anhand seines Namens und ruft die on_activate()-Methode auf."""
        if module_name in self.modules:  # Prüfen, ob das Modul geladen ist
            self.modules[module_name].on_activate()  # Aktivierung aufrufen

    def deactivate_module(self, module_name):  # Methode zum Deaktivieren eines Moduls nach Namen
        """Deaktiviert ein Modul anhand seines Namens und ruft die on_deactivate()-Methode auf."""
        if module_name in self.modules:  # Prüfen, ob das Modul geladen ist
            self.modules[module_name].on_deactivate()  # Deaktivierung aufrufen

# Definition der Menü-Klassen für die Tabs als Platzhalter-Widgets
class SettingsMenu(QWidget):  # Platzhalter-Klasse für das Einstellungsmenü
    """Widget für das Einstellungsmenü des Hauptfensters."""
    def __init__(self, parent=None):  # Konstruktor: Aufbau der UI-Komponenten
        super().__init__(parent)  # Aufruf des Elternkonstruktors
        layout = QVBoxLayout(self)  # Vertikales Layout erstellen
        layout.addWidget(QLabel("Einstellungsmenü"))  # Platzhalter-Label hinzufügen

class ReportingMenu(QWidget):  # Platzhalter-Klasse für das Berichtswesen
    """Widget für die Berichtsanzeige und den Export."""
    def __init__(self, parent=None):  # Konstruktor: Aufbau der UI-Komponenten
        super().__init__(parent)  # Aufruf des Elternkonstruktors
        layout = QVBoxLayout(self)  # Vertikales Layout erstellen
        layout.addWidget(QLabel("Berichtsanzeige"))  # Platzhalter-Label hinzufügen

class ModuleMenu(QWidget):  # Platzhalter-Klasse für die Modul-Verwaltung
    """Widget für die Auswahl und Verwaltung der Module."""
    def __init__(self, parent=None):  # Konstruktor: Aufbau der UI-Komponenten
        super().__init__(parent)  # Aufruf des Elternkonstruktors
        layout = QVBoxLayout(self)  # Vertikales Layout erstellen
        layout.addWidget(QLabel("Modulverwaltung"))  # Platzhalter-Label hinzufügen
