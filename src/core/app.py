# Datei: src/core/app.py – Hauptanwendung mit Tab-basierter Navigation
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QStackedWidget  # Import Qt-Widgets und Button-Layout mit StackedWidget
from PySide6.QtCore import Qt  # Import Qt-Kernfunktionen fürs Alignment
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

        # Begrüßungstext anzeigen
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")  # QLabel für Willkommensnachricht
        welcome_label.setAlignment(Qt.AlignCenter)  # Zentrieren des Textes
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")  # Stil anpassen
        self.layout.addWidget(welcome_label)  # Begrüßung in das Layout einfügen

        # Buttons für Einstellungen, Berichte und Module
        button_layout = QHBoxLayout()  # Horizontales Layout für Buttons
        button_layout.addStretch(1)  # linker Abstand für Zentrierung
        settings_btn = QPushButton("Einstellungen")  # Button für Einstellungen
        reporting_btn = QPushButton("Berichte")  # Button für Berichte
        modules_btn = QPushButton("Module")  # Button für Module
        button_layout.addWidget(settings_btn)
        button_layout.addWidget(reporting_btn)
        button_layout.addWidget(modules_btn)
        button_layout.addStretch(1)  # rechter Abstand für Zentrierung
        self.layout.addLayout(button_layout)  # Füge das Button-Layout ins Hauptlayout ein

        # Untermenüs als gestapeltes Widget einrichten
        self.stack = QStackedWidget()  # StackedWidget für Untermenüs
        # Settings-Seite erstellen
        self.settings_page = QWidget()  # Container für Einstellungen
        settings_layout = QVBoxLayout(self.settings_page)  # Layout für Settings-Seite
        settings_layout.addWidget(QLabel("Einstellungen-Übersicht"))  # Platzhalter-Text
        # Reporting-Seite erstellen
        self.reporting_page = QWidget()  # Container für Berichte
        reporting_layout = QVBoxLayout(self.reporting_page)  # Layout für Reporting-Seite
        reporting_layout.addWidget(QLabel("Berichte-Übersicht"))  # Platzhalter-Text
        # Module-Seite erstellen
        self.module_page = QWidget()  # Container für Module
        module_layout = QVBoxLayout(self.module_page)  # Layout für Module-Seite
        module_layout.addWidget(QLabel("Module-Übersicht"))  # Platzhalter-Text
        # Seiten zum Stack hinzufügen
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.reporting_page)
        self.stack.addWidget(self.module_page)
        # Standardseite festlegen
        self.stack.setCurrentWidget(self.settings_page)
        # Button-Klicks mit Seitenwechsel verbinden
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        reporting_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        modules_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        # Gestapeltes Widget ins Hauptlayout einfügen
        self.layout.addWidget(self.stack)
