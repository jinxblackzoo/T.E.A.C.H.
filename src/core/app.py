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

        # QStackedWidget für alle Seiten (wie KLAR)
        self.stack = QStackedWidget()  # Gestapeltes Widget für Menüführung
        self.setCentralWidget(self.stack)  # Stack ist jetzt das Zentral-Widget

        # Hauptmenü-Seite (wie KLAR)
        self.menu_page = QWidget()  # Widget für das Hauptmenü
        menu_layout = QVBoxLayout(self.menu_page)  # Vertikales Layout für das Hauptmenü
        menu_layout.setAlignment(Qt.AlignCenter)  # Zentriere alles vertikal und horizontal
        # Begrüßung oben
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")  # Begrüßung
        welcome_label.setAlignment(Qt.AlignCenter)  # Zentriert
        welcome_label.setStyleSheet("font-size: 28px; font-weight: bold; margin: 24px;")
        menu_layout.addWidget(welcome_label)
        subtitle_label = QLabel("Toll ein anderes chaotisches Hilfeprogramm")  # Untertitel
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 18px; margin-bottom: 36px;")
        menu_layout.addWidget(subtitle_label)
        # Große, übersichtliche Buttons für die Menüpunkte
        settings_btn = QPushButton("Einstellungen")
        settings_btn.setMinimumHeight(48)
        settings_btn.setStyleSheet("font-size: 20px; margin: 16px 0;")
        menu_layout.addWidget(settings_btn)
        reporting_btn = QPushButton("Berichte")
        reporting_btn.setMinimumHeight(48)
        reporting_btn.setStyleSheet("font-size: 20px; margin: 16px 0;")
        menu_layout.addWidget(reporting_btn)
        modules_btn = QPushButton("Module")
        modules_btn.setMinimumHeight(48)
        modules_btn.setStyleSheet("font-size: 20px; margin: 16px 0;")
        menu_layout.addWidget(modules_btn)
        menu_layout.addStretch(1)  # Abstand nach unten

        # Einstellungen-Seite
        self.settings_page = QWidget()
        settings_layout = QVBoxLayout(self.settings_page)
        settings_layout.setAlignment(Qt.AlignCenter)
        settings_label = QLabel("Einstellungen")
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        settings_layout.addWidget(settings_label)
        general_btn = QPushButton("Allgemein")
        general_btn.setMinimumHeight(40)
        general_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        settings_layout.addWidget(general_btn)
        user_btn = QPushButton("Benutzer")
        user_btn.setMinimumHeight(40)
        user_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        settings_layout.addWidget(user_btn)
        back_btn = QPushButton("Zurück")
        back_btn.setMinimumHeight(40)
        back_btn.setStyleSheet("font-size: 16px; margin: 24px 0;")
        settings_layout.addWidget(back_btn)

        # Berichte-Seite
        self.reporting_page = QWidget()
        reporting_layout = QVBoxLayout(self.reporting_page)
        reporting_layout.setAlignment(Qt.AlignCenter)
        reporting_label = QLabel("Berichte")
        reporting_label.setAlignment(Qt.AlignCenter)
        reporting_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        reporting_layout.addWidget(reporting_label)
        export_btn = QPushButton("Exportieren")
        export_btn.setMinimumHeight(40)
        export_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        reporting_layout.addWidget(export_btn)
        back_btn_r = QPushButton("Zurück")
        back_btn_r.setMinimumHeight(40)
        back_btn_r.setStyleSheet("font-size: 16px; margin: 24px 0;")
        reporting_layout.addWidget(back_btn_r)

        # Module-Seite
        self.module_page = QWidget()
        module_layout = QVBoxLayout(self.module_page)
        module_layout.setAlignment(Qt.AlignCenter)
        module_label = QLabel("Module")
        module_label.setAlignment(Qt.AlignCenter)
        module_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        module_layout.addWidget(module_label)
        add_btn = QPushButton("Modul hinzufügen")
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        module_layout.addWidget(add_btn)
        back_btn_m = QPushButton("Zurück")
        back_btn_m.setMinimumHeight(40)
        back_btn_m.setStyleSheet("font-size: 16px; margin: 24px 0;")
        module_layout.addWidget(back_btn_m)

        # Seiten zum Stack hinzufügen
        self.stack.addWidget(self.menu_page)         # Index 0: Hauptmenü
        self.stack.addWidget(self.settings_page)     # Index 1: Einstellungen
        self.stack.addWidget(self.reporting_page)    # Index 2: Berichte
        self.stack.addWidget(self.module_page)       # Index 3: Module
        self.stack.setCurrentWidget(self.menu_page)  # Starte mit Hauptmenü

        # Navigation: Buttons verbinden
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        reporting_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        modules_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        back_btn_r.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        back_btn_m.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))

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
