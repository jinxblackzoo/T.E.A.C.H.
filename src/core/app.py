# Datei: src/core/app.py – Hauptanwendung mit Tab-basierter Navigation
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QStackedWidget  # Import Qt-Widgets und Button-Layout mit StackedWidget
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
        welcome_label = QLabel("Toll ein anderes chaotisches Hilfeprogramm")
        welcome_label.setAlignment(Qt.AlignCenter)  # Zentrieren des Textes
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")  # Stil anpassen
        self.layout.addWidget(welcome_label)  # Begrüßung in das Layout einfügen

        # Buttons für Einstellungen, Berichte und Module
        button_layout = QVBoxLayout()  # Vertikales Layout für Buttons
        button_layout.setAlignment(Qt.AlignHCenter)  # Buttons horizontal zentrieren
        settings_btn = QPushButton("Einstellungen")  # Button für Einstellungen
        reporting_btn = QPushButton("Berichte")  # Button für Berichte
        modules_btn = QPushButton("Module")  # Button für Module
        button_layout.addWidget(settings_btn)  # Einstellungen hinzufügen
        button_layout.addWidget(reporting_btn)  # Berichte hinzufügen
        button_layout.addWidget(modules_btn)  # Module hinzufügen
        self.layout.addLayout(button_layout)  # Füge das vertikale Button-Layout ein

        # Untermenüs als gestapeltes Widget einrichten
        self.stack = QStackedWidget()  # StackedWidget für Untermenüs
        # Einstellungen-Menü als eigene Seite mit Buttons
        self.settings_page = QWidget()  # Widget für die Einstellungen-Seite
        settings_layout = QVBoxLayout(self.settings_page)  # Vertikales Layout für die Einstellungen
        settings_layout.setAlignment(Qt.AlignHCenter)  # Zentriere die Buttons horizontal
        # Überschrift für das Einstellungsmenü
        settings_label = QLabel("Einstellungen")  # Überschrift
        settings_label.setAlignment(Qt.AlignCenter)  # Zentriert
        settings_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 16px;")  # Stil
        settings_layout.addWidget(settings_label)  # Überschrift hinzufügen
        # Menü-Buttons für verschiedene Einstellungsbereiche
        general_btn = QPushButton("Allgemein")  # Button für allgemeine Einstellungen
        user_btn = QPushButton("Benutzer")  # Button für Benutzer-Einstellungen
        back_btn = QPushButton("Zurück")  # Button zum Zurückkehren ins Hauptmenü
        settings_layout.addWidget(general_btn)  # Füge Button für Allgemein hinzu
        settings_layout.addWidget(user_btn)  # Füge Button für Benutzer hinzu
        settings_layout.addWidget(back_btn)  # Füge Zurück-Button hinzu
        # Logik für Zurück-Button: Wechsel ins Hauptmenü (Settings als Startseite)
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))  # Zurück ins Hauptmenü
        # Die Seite für das Hauptmenü referenzieren (siehe unten)

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
