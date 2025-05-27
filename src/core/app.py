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

        # Hauptmenü-Seite gemäß .mm-Vorgabe
        self.menu_page = QWidget()  # Widget für das Hauptmenü
        menu_layout = QVBoxLayout(self.menu_page)  # Vertikales Layout für das Hauptmenü
        menu_layout.setAlignment(Qt.AlignCenter)  # Zentriere alles vertikal und horizontal

        # Begrüßungstext
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")  # Überschrift
        welcome_label.setAlignment(Qt.AlignCenter)  # Zentriert
        welcome_label.setStyleSheet("font-size: 28px; font-weight: bold; margin: 24px;")  # Groß und prominent
        menu_layout.addWidget(welcome_label)
        subtitle_label = QLabel("Toll ein anderes chaotisches Hilfeprogramm")  # Untertitel
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 18px; margin-bottom: 36px;")  # Stil wie besprochen
        menu_layout.addWidget(subtitle_label)

        # Drei Hauptmenü-Buttons gemäß .mm:
        # 1. Einstellungen
        settings_btn = QPushButton("Einstellungen")  # Button für Einstellungen
        settings_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        settings_btn.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 250px;
        """)  # Einheitliches Design für alle Hauptmenü-Buttons
        menu_layout.addWidget(settings_btn)

        # 2. Reporting
        reporting_btn = QPushButton("Reporting")  # Button für Reporting
        reporting_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        reporting_btn.setStyleSheet(settings_btn.styleSheet())  # Gleiches Design wie Einstellungen-Button
        menu_layout.addWidget(reporting_btn)

        # 3. Module
        modules_btn = QPushButton("Module")  # Button für Module
        modules_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        modules_btn.setStyleSheet(settings_btn.styleSheet())  # Gleiches Design wie Einstellungen-Button
        menu_layout.addWidget(modules_btn)
        
        menu_layout.addStretch(1)  # Abstand nach unten für ein aufgeräumtes Layout


        # Einstellungen-Seite 
        self.settings_page = QWidget()  # Widget für die Einstellungen-Seite
        settings_layout = QVBoxLayout(self.settings_page)  # Vertikales Layout für Einstellungen
        settings_layout.setAlignment(Qt.AlignCenter)  # Zentriert alles
        # Überschrift für Einstellungen
        settings_label = QLabel("Einstellungen")  # Überschrift
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        settings_layout.addWidget(settings_label)
        # Button für KI-Einstellungen (führt zu KI-Einstellungen-Seite)
        ai_settings_btn = QPushButton("KI-Einstellungen")
        ai_settings_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        ai_settings_btn.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Einstellungs-Buttons
        settings_layout.addWidget(ai_settings_btn)

        # Zurück-Button zum Hauptmenü
        back_btn_settings = QPushButton("Zurück zum Hauptmenü")
        back_btn_settings.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_settings.setStyleSheet(ai_settings_btn.styleSheet())  # Gleiches Design wie KI-Einstellungen-Button
        settings_layout.addWidget(back_btn_settings)
        # KI-Einstellungen-Seite (Platzhalter für spätere Untermenüs)
        self.ai_settings_page = QWidget()
        ai_settings_layout = QVBoxLayout(self.ai_settings_page)
        ai_settings_layout.setAlignment(Qt.AlignCenter)
        ai_settings_label = QLabel("KI-Einstellungen")
        ai_settings_label.setAlignment(Qt.AlignCenter)
        ai_settings_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        ai_settings_layout.addWidget(ai_settings_label)
        # Zurück-Button zu Einstellungen
        back_btn_ai = QPushButton("Zurück zu Einstellungen")
        back_btn_ai.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_ai.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Einstellungs-Buttons
        ai_settings_layout.addWidget(back_btn_ai)
        # Seiten zum Stack hinzufügen
        self.stack.addWidget(self.menu_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.ai_settings_page)
        # Navigation: Buttons verbinden
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        ai_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.ai_settings_page))
        back_btn_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        back_btn_ai.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))

        # Reporting-Seite gemäß .mm-Vorgabe
        self.reporting_page = QWidget()  # Widget für das Reporting-Menü
        reporting_layout = QVBoxLayout(self.reporting_page)  # Vertikales Layout für Reporting
        reporting_layout.setAlignment(Qt.AlignCenter)  # Zentriert alles
        # Überschrift für Reporting
        reporting_label = QLabel("Reporting")  # Überschrift
        reporting_label.setAlignment(Qt.AlignCenter)
        reporting_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        reporting_layout.addWidget(reporting_label)
        # Button für Report als PDF drucken
        print_report_btn = QPushButton("Report als PDF drucken")
        print_report_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        print_report_btn.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 350px;
        """)  # Einheitliches Design für Reporting-Buttons
        reporting_layout.addWidget(print_report_btn)

        # Button für Anzeige des aktuellen Status
        status_btn = QPushButton("Anzeige des aktuellen Status")
        status_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        status_btn.setStyleSheet(print_report_btn.styleSheet())  # Gleiches Design wie PDF-Button
        reporting_layout.addWidget(status_btn)

        # Zurück-Button zum Hauptmenü
        back_btn_reporting = QPushButton("Zurück zum Hauptmenü")
        back_btn_reporting.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_reporting.setStyleSheet(print_report_btn.styleSheet())  # Gleiches Design wie PDF-Button
        reporting_layout.addWidget(back_btn_reporting)
        # Platzhalterseiten für die beiden Unterseiten
        self.print_report_page = QWidget()
        print_report_layout = QVBoxLayout(self.print_report_page)
        print_report_layout.setAlignment(Qt.AlignCenter)
        print_report_label = QLabel("Report als PDF drucken")
        print_report_label.setAlignment(Qt.AlignCenter)
        print_report_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        print_report_layout.addWidget(print_report_label)
        back_btn_pr = QPushButton("Zurück zu Reporting")
        back_btn_pr.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_pr.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Zurück-Buttons
        print_report_layout.addWidget(back_btn_pr)
        
        self.status_page = QWidget()
        status_layout = QVBoxLayout(self.status_page)
        status_layout.setAlignment(Qt.AlignCenter)
        status_label = QLabel("Anzeige des aktuellen Status")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        status_layout.addWidget(status_label)
        back_btn_s = QPushButton("Zurück zu Reporting")
        back_btn_s.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_s.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Zurück-Buttons
        status_layout.addWidget(back_btn_s)
        
        # Module-Seite gemäß .mm-Vorgabe
        self.module_page = QWidget()  # Widget für die Module-Seite
        module_layout = QVBoxLayout(self.module_page)  # Vertikales Layout für Module
        module_layout.setAlignment(Qt.AlignCenter)  # Zentriert alles
        # Überschrift für Module
        module_label = QLabel("Module")  # Überschrift
        module_label.setAlignment(Qt.AlignCenter)
        module_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        module_layout.addWidget(module_label)
        # Button für VOLL Vokabeltrainer
        voll_btn = QPushButton("VOLL Vokabeltrainer")
        voll_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        voll_btn.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 350px;
        """)  # Einheitliches Design für Modul-Buttons
        module_layout.addWidget(voll_btn)

        # Button für MUT Einheitentrainer
        mut_btn = QPushButton("MUT Einheitentrainer")
        mut_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        mut_btn.setStyleSheet(voll_btn.styleSheet())  # Gleiches Design wie VOLL-Button
        module_layout.addWidget(mut_btn)

        # Button für KLAR Karteikartentrainer
        klar_btn = QPushButton("KLAR Karteikartentrainer")
        klar_btn.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        klar_btn.setStyleSheet(voll_btn.styleSheet())  # Gleiches Design wie VOLL-Button
        module_layout.addWidget(klar_btn)

        # Zurück-Button zum Hauptmenü
        back_btn_m = QPushButton("Zurück zum Hauptmenü")
        back_btn_m.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_m.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Zurück-Buttons
        module_layout.addWidget(back_btn_m)
        module_layout.addStretch(1)  # Abstand nach unten
        # Platzhalterseiten für die drei Module
        self.voll_page = QWidget()
        voll_layout = QVBoxLayout(self.voll_page)
        voll_layout.setAlignment(Qt.AlignCenter)
        voll_label = QLabel("VOLL Vokabeltrainer")
        voll_label.setAlignment(Qt.AlignCenter)
        voll_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        voll_layout.addWidget(voll_label)
        back_btn_voll = QPushButton("Zurück zu Module")
        back_btn_voll.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_voll.setStyleSheet("""
            font-size: 20px;
            margin: 20px 0;
            min-width: 300px;
        """)  # Einheitliches Design für Zurück-Buttons
        voll_layout.addWidget(back_btn_voll)
        self.mut_page = QWidget()
        mut_layout = QVBoxLayout(self.mut_page)
        mut_layout.setAlignment(Qt.AlignCenter)
        mut_label = QLabel("MUT Einheitentrainer")
        mut_label.setAlignment(Qt.AlignCenter)
        mut_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        mut_layout.addWidget(mut_label)
        back_btn_mut = QPushButton("Zurück zu Module")
        back_btn_mut.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_mut.setStyleSheet(back_btn_voll.styleSheet())  # Gleiches Design wie VOLL-Zurück-Button
        mut_layout.addWidget(back_btn_mut)
        self.klar_page = QWidget()
        klar_layout = QVBoxLayout(self.klar_page)
        klar_layout.setAlignment(Qt.AlignCenter)
        klar_label = QLabel("KLAR Karteikartentrainer")
        klar_label.setAlignment(Qt.AlignCenter)
        klar_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 24px;")
        klar_layout.addWidget(klar_label)
        back_btn_klar = QPushButton("Zurück zu Module")
        back_btn_klar.setMinimumHeight(55)  # Mindesthöhe 55 Pixel
        back_btn_klar.setStyleSheet(back_btn_voll.styleSheet())  # Gleiches Design wie VOLL-Zurück-Button
        klar_layout.addWidget(back_btn_klar)

        
        # Seiten zum Stack hinzufügen
        self.stack.addWidget(self.menu_page)         # Index 0: Hauptmenü
        self.stack.addWidget(self.settings_page)     # Index 1: Einstellungen
        self.stack.addWidget(self.ai_settings_page)   # Index 2: KI-Einstellungen
        self.stack.addWidget(self.reporting_page)    # Index 3: Berichte
        self.stack.addWidget(self.print_report_page) # Index 4: Report als PDF drucken
        self.stack.addWidget(self.status_page)       # Index 5: Anzeige des aktuellen Status
        self.stack.addWidget(self.module_page)       # Index 6: Module
        self.stack.addWidget(self.voll_page)         # Index 7: VOLL Vokabeltrainer
        self.stack.addWidget(self.mut_page)          # Index 8: MUT Einheitentrainer
        self.stack.addWidget(self.klar_page)         # Index 9: KLAR Karteikartentrainer
        self.stack.setCurrentWidget(self.menu_page)  # Starte mit Hauptmenü

        # Navigation: Buttons verbinden
        # Hauptmenü-Buttons
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        reporting_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        modules_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        
        # Einstellungen-Buttons
        ai_settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.ai_settings_page))
        back_btn_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        back_btn_ai.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        
        # Reporting-Buttons
        print_report_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.print_report_page))
        status_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.status_page))
        back_btn_reporting.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        
        # Modul-Buttons
        voll_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.voll_page))
        mut_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.mut_page))
        klar_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.klar_page))
        back_btn_m.clicked.connect(lambda: self.stack.setCurrentWidget(self.menu_page))
        
        # Zurück-Buttons in den Modul-Seiten
        back_btn_voll.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        back_btn_mut.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        back_btn_klar.clicked.connect(lambda: self.stack.setCurrentWidget(self.module_page))
        
        # Zurück-Buttons in den Reporting-Seiten
        back_btn_pr.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
        back_btn_s.clicked.connect(lambda: self.stack.setCurrentWidget(self.reporting_page))
