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
        # QStackedWidget für alle Seiten (wie KLAR)
        self.stack = QStackedWidget()  # Gestapeltes Widget für Menüführung
        self.setCentralWidget(self.stack)  # Stack ist das Zentral-Widget

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
        
        # Untermenü für Berichte
        reporting_submenu_layout = QVBoxLayout()
        reporting_submenu_layout.setAlignment(Qt.AlignCenter)
        reporting_submenu_label = QLabel("Berichte-Menü")
        reporting_submenu_label.setAlignment(Qt.AlignCenter)
        reporting_submenu_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 16px;")
        reporting_submenu_layout.addWidget(reporting_submenu_label)
        
        # Button für Report als PDF drucken
        print_report_btn = QPushButton("Report als PDF drucken")
        print_report_btn.setMinimumHeight(40)
        print_report_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        reporting_submenu_layout.addWidget(print_report_btn)
        
        # Button für Anzeige des aktuellen Status
        status_btn = QPushButton("Anzeige des aktuellen Status")
        status_btn.setMinimumHeight(40)
        status_btn.setStyleSheet("font-size: 16px; margin: 8px 0;")
        reporting_submenu_layout.addWidget(status_btn)
        
        # Zurück-Button
        back_btn_r = QPushButton("Zurück")
        back_btn_r.setMinimumHeight(40)
        back_btn_r.setStyleSheet("font-size: 16px; margin: 24px 0;")
        reporting_submenu_layout.addWidget(back_btn_r)
        
        reporting_layout.addLayout(reporting_submenu_layout)
        
        # Seiten für das Untermenü
        self.print_report_page = QWidget()
        print_report_layout = QVBoxLayout(self.print_report_page)
        print_report_layout.setAlignment(Qt.AlignCenter)
        print_report_label = QLabel("Report als PDF drucken")
        print_report_label.setAlignment(Qt.AlignCenter)
        print_report_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        print_report_layout.addWidget(print_report_label)
        back_btn_pr = QPushButton("Zurück")
        back_btn_pr.setMinimumHeight(40)
        back_btn_pr.setStyleSheet("font-size: 16px; margin: 24px 0;")
        print_report_layout.addWidget(back_btn_pr)
        
        self.status_page = QWidget()
        status_layout = QVBoxLayout(self.status_page)
        status_layout.setAlignment(Qt.AlignCenter)
        status_label = QLabel("Anzeige des aktuellen Status")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        status_layout.addWidget(status_label)
        back_btn_s = QPushButton("Zurück")
        back_btn_s.setMinimumHeight(40)
        back_btn_s.setStyleSheet("font-size: 16px; margin: 24px 0;")
        status_layout.addWidget(back_btn_s)
        
        # Module-Seite
        self.module_page = QWidget()  # Container für Module
        module_layout = QVBoxLayout(self.module_page)  # Layout für Module-Seite
        module_layout.setAlignment(Qt.AlignCenter)  # Zentriere alles vertikal und horizontal
        module_label = QLabel("Module")  # Überschrift
        module_label.setAlignment(Qt.AlignCenter)  # Zentriert
        module_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        module_layout.addWidget(module_label)
        module_layout.addStretch(1)  # Abstand nach unten
        
        # Seiten zum Stack hinzufügen
        self.stack.addWidget(self.menu_page)         # Index 0: Hauptmenü
        self.stack.addWidget(self.settings_page)     # Index 1: Einstellungen
        self.stack.addWidget(self.reporting_page)    # Index 2: Berichte
        self.stack.addWidget(self.module_page)       # Index 3: Module
        self.stack.addWidget(self.print_report_page) # Index 4: Report als PDF drucken
        self.stack.addWidget(self.status_page)       # Index 5: Anzeige des aktuellen Status
        self.stack.setCurrentWidget(self.menu_page)  # Starte mit Hauptmenü

        # Navigation: Buttons verbinden
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        reporting_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        modules_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        back_btn_r.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        print_report_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.print_report_page))
        status_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.status_page))
        back_btn_pr.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        back_btn_s.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
