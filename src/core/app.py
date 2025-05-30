# Datei: src/core/app.py – Hauptanwendung mit Tab-basierter Navigation
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QStackedWidget, QTextEdit, QScrollArea, QFileDialog
from PySide6.QtCore import Qt  # Import Qt-Kernfunktionen fürs Alignment
from PySide6.QtGui import QPdfWriter, QTextDocument, QPageLayout
from datetime import datetime
import json
from .module import TEACHModule  # Import der Basisklasse für Module

class TEACH(QMainWindow):  # Definition der Hauptfensterklasse, erbt von QMainWindow
    """Hauptfenster der T.E.A.C.H. Anwendung mit Tab-Navigation."""
    
    # Zentrale Stildefinitionen
    # Layout-Einstellungen für alle Seiten
    LAYOUT_STYLE = {
        'alignment': Qt.AlignTop | Qt.AlignHCenter,  # Oben zentriert
        'spacing': 20,                              # Abstand zwischen Widgets
        'margins': (0, 20, 0, 0),                   # Rand oben 20px, sonst 0
        'title_style': 'font-size: 24px; font-weight: bold; margin: 24px 0;',
        'subtitle_style': 'font-size: 18px; margin-bottom: 36px;',
        'content_margins': (40, 20, 40, 20)        # Innenabstand für Inhaltscontainer
    }
    
    # Zentrale Stildefinition für alle Buttons in der Anwendung
    # Dies stellt sicher, dass alle Buttons ein einheitliches Erscheinungsbild haben
    # BUTTON_STYLE definiert das Aussehen aller Buttons
    BUTTON_STYLE = """
        QPushButton {
            font-size: 20px;
            min-height: 60px;
            min-width: 60px;
            margin: 10px 10;
            padding: 10px 10px;
            background-color: #990099;
            border-radius: 16px; 
        }
    """
    # font-size: Schriftgröße der Button-Beschriftung
    # min-height: Minimale Höhe des Buttons in Pixeln
    # min-width: Minimale Breite des Buttons in Pixeln
    # margin: Äußerer Abstand oben und unten (20px), links/rechts (0)
    # padding: Innenabstand des Buttons (20px oben/unten, 20px links/rechts)
    # background-color: Hintergrundfarbe des Buttons
    # border-radius: Abrundung der Ecken des Buttons (hier 18px)
    
    # BACK_BUTTON_STYLE: Spezielles Stylesheet für alle Zurück-Buttons
    # - Hintergrundfarbe: abgesetztes helles Grau
    # - Schriftgröße: wie Hauptbuttons
    # - Ecken: stärker abgerundet
    # - Pfeil als Text: "←"
    BACK_BUTTON_STYLE = """
        QPushButton {
            font-size: 15px;
            min-height: 20px;
            min-width: 20px;
            margin: 10px 0;
            padding: 10px 10px;
            background-color: #62B0F5;
            border-radius: 15px;
        }
    """
    # background-color: helles Grau für Zurück-Buttons
    # border-radius: stärker abgerundet (24px)
    # font-size, min-height, min-width, margin, padding: analog zu BUTTON_STYLE

    def create_button(self, text=None, style="default"):
        """
        Zentrale Hilfsfunktion zur Erstellung von Buttons mit einheitlichem Design.
        - style="default": Standard-Button mit zentralem BUTTON_STYLE
        - style="back":   Zurück-Button mit Pfeil und BACK_BUTTON_STYLE
        - text:            Optionaler Text (bei None wird für Zurück-Button automatisch der Pfeil verwendet)
        Gibt einen QPushButton mit passendem Style und Text zurück.
        """
        btn = QPushButton()
        if style == "back":
            btn.setText("←" if text is None else text)  # Standardmäßig Pfeil
            btn.setStyleSheet(self.BACK_BUTTON_STYLE)
        else:
            btn.setText(text if text else "")
            btn.setStyleSheet(self.BUTTON_STYLE)
        return btn
    
    def __init__(self):  # Konstruktor: Einrichtung des Fensters und der UI-Komponenten
        super().__init__()  # Aufruf des Elternkonstruktors
        self.setWindowTitle("T.E.A.C.H. - Toll Ein Anderes Chaotisches Hilfeprogramm")  # Fenstertitel setzen
        self.setGeometry(100, 100, 1024, 768)  # Position und Größe des Fensters definieren

        # Zentrales Widget und Layout anlegen
        self.central_widget = QWidget()  # Hauptcontainer-Widget
        main_layout = QVBoxLayout(self.central_widget)  # Hauptlayout für zentrierte Ausrichtung
        main_layout.setAlignment(Qt.AlignCenter)  # Zentriert den Inhalt
        
        # Container für zentrierten Inhalt
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # QStackedWidget für alle Seiten
        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(content_widget)
        self.setCentralWidget(self.central_widget)  # Setzt das Hauptwidget

        # Setze das zentrale Button-Stylesheet global auf das Hauptfenster
        # Dadurch wird sichergestellt, dass alle QPushButton-Elemente im Fenster das Stylesheet erhalten
        # Dies hilft, Fehler durch lokale Überschreibungen oder falsche Anwendung zu vermeiden
        self.setStyleSheet(self.BUTTON_STYLE)

        # Hauptmenü-Seite gemäß .mm-Vorgabe
        self.menu_page = QWidget()
        menu_outer_layout = QVBoxLayout(self.menu_page)
        menu_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        menu_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        menu_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        # Container für zentrierten Inhalt
        menu_container = QWidget()
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        menu_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        menu_outer_layout.addWidget(menu_container, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Begrüßungstext
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        menu_layout.addWidget(welcome_label)
        
        subtitle_label = QLabel("Toll ein anderes chaotisches Hilfeprogramm")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(self.LAYOUT_STYLE['subtitle_style'])
        menu_layout.addWidget(subtitle_label)

        # Drei Hauptmenü-Buttons gemäß .mm:
        # 1. Einstellungen
        # Hauptmenü-Buttons mit zentraler Button-Funktion
        settings_btn = self.create_button("Einstellungen")
        menu_layout.addWidget(settings_btn)
        reporting_btn = self.create_button("Reporting")
        menu_layout.addWidget(reporting_btn)
        modules_btn = self.create_button("Module")
        menu_layout.addWidget(modules_btn)
        
        menu_layout.addStretch(1)  # Abstand nach unten für ein aufgeräumtes Layout


        # Einstellungen-Seite 
        self.settings_page = QWidget()
        settings_outer_layout = QVBoxLayout(self.settings_page)
        settings_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        settings_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        settings_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        # Container für zentrierten Inhalt
        settings_container = QWidget()
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        settings_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        settings_outer_layout.addWidget(settings_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Überschrift für Einstellungen
        settings_label = QLabel("Einstellungen")
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        settings_layout.addWidget(settings_label)
        # Button für KI-Einstellungen (führt zu KI-Einstellungen-Seite)
        # KI-Einstellungen-Button mit zentraler Button-Funktion
        ai_settings_btn = self.create_button("KI-Einstellungen")
        settings_layout.addWidget(ai_settings_btn)

        # Zurück-Button zum Hauptmenü
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_settings = self.create_button(style="back")
        settings_layout.addWidget(back_btn_settings)
        # KI-Einstellungen-Seite
        self.ai_settings_page = QWidget()
        ai_outer_layout = QVBoxLayout(self.ai_settings_page)
        ai_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        ai_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        ai_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        # Container für zentrierten Inhalt
        ai_container = QWidget()
        ai_settings_layout = QVBoxLayout(ai_container)
        ai_settings_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        ai_settings_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        ai_outer_layout.addWidget(ai_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Überschrift für KI-Einstellungen
        ai_settings_label = QLabel("KI-Einstellungen")
        ai_settings_label.setAlignment(Qt.AlignCenter)
        ai_settings_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        ai_settings_layout.addWidget(ai_settings_label)
        # Zurück-Button zu Einstellungen
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_ai = self.create_button(style="back")
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
        self.reporting_page = QWidget()
        reporting_outer_layout = QVBoxLayout(self.reporting_page)
        reporting_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        reporting_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        reporting_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        # Container für zentrierten Inhalt
        reporting_container = QWidget()
        reporting_layout = QVBoxLayout(reporting_container)
        reporting_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        reporting_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        reporting_outer_layout.addWidget(reporting_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Überschrift für Reporting
        reporting_label = QLabel("Reporting")
        reporting_label.setAlignment(Qt.AlignCenter)
        reporting_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        reporting_layout.addWidget(reporting_label)
        # Button für Report als PDF drucken
        # Reporting-Menü-Buttons mit zentraler Button-Funktion
        print_report_btn = self.create_button("Report als PDF drucken")
        reporting_layout.addWidget(print_report_btn)
        status_btn = self.create_button("Status anzeigen")
        reporting_layout.addWidget(status_btn)

        # Zurück-Button zum Hauptmenü
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_reporting = self.create_button(style="back")
        reporting_layout.addWidget(back_btn_reporting)
        # Platzhalterseiten für die beiden Unterseiten
        # PDF-Druckseite
        self.print_report_page = QWidget()
        print_report_outer_layout = QVBoxLayout(self.print_report_page)
        print_report_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        print_report_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        print_report_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        print_report_container = QWidget()
        print_report_layout = QVBoxLayout(print_report_container)
        print_report_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        print_report_outer_layout.addWidget(print_report_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        print_report_label = QLabel("Report als PDF drucken")
        print_report_label.setAlignment(Qt.AlignCenter)
        print_report_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        print_report_layout.addWidget(print_report_label)
        
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_pr = self.create_button(style="back")
        print_report_layout.addWidget(back_btn_pr)
        
        # Statusseite
        self.status_page = QWidget()
        status_layout = QVBoxLayout(self.status_page)
        status_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        status_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        status_label = QLabel("Anzeige des aktuellen Status")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        status_layout.addWidget(status_label)
        # ScrollArea zur Anzeige von Modul-Reports
        self.report_scroll = QScrollArea()
        self.report_scroll.setWidgetResizable(True)
        status_layout.addWidget(self.report_scroll)
        
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_s = self.create_button(style="back")
        status_layout.addWidget(back_btn_s)
        
        # Module-Seite gemäß .mm-Vorgabe
        self.module_page = QWidget()
        module_outer_layout = QVBoxLayout(self.module_page)
        module_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        module_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        module_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        # Container für zentrierten Inhalt
        module_container = QWidget()
        module_layout = QVBoxLayout(module_container)
        module_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        module_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        module_outer_layout.addWidget(module_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Überschrift für Module
        module_label = QLabel("Module")
        module_label.setAlignment(Qt.AlignCenter)
        module_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        module_layout.addWidget(module_label)
        
        # Button für VOLL Vokabeltrainer
        # Modul-Buttons mit zentraler Button-Funktion
        voll_btn = self.create_button("VOLL Vokabeltrainer")
        module_layout.addWidget(voll_btn)
        mut_btn = self.create_button("MUT Einheitentrainer")
        module_layout.addWidget(mut_btn)
        klar_btn = self.create_button("KLAR Karteikartentrainer")
        module_layout.addWidget(klar_btn)
        
        # Zurück-Button zum Hauptmenü
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_m = self.create_button(style="back")
        module_layout.addWidget(back_btn_m)
        
        # VOLL Vokabeltrainer Seite
        self.voll_page = QWidget()
        voll_outer_layout = QVBoxLayout(self.voll_page)
        voll_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        voll_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        voll_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        voll_container = QWidget()
        voll_layout = QVBoxLayout(voll_container)
        voll_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        voll_outer_layout.addWidget(voll_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        voll_label = QLabel("VOLL Vokabeltrainer")
        voll_label.setAlignment(Qt.AlignCenter)
        voll_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        voll_layout.addWidget(voll_label)
        
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_voll = self.create_button(style="back")
        voll_layout.addWidget(back_btn_voll)
        
        # MUT Einheitentrainer Seite
        self.mut_page = QWidget()
        mut_outer_layout = QVBoxLayout(self.mut_page)
        mut_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        mut_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        mut_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        mut_container = QWidget()
        mut_layout = QVBoxLayout(mut_container)
        mut_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        mut_outer_layout.addWidget(mut_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        mut_label = QLabel("MUT Einheitentrainer")
        mut_label.setAlignment(Qt.AlignCenter)
        mut_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        mut_layout.addWidget(mut_label)
        
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_mut = self.create_button(style="back")
        mut_layout.addWidget(back_btn_mut)
        
        # KLAR Karteikartentrainer Seite
        self.klar_page = QWidget()
        klar_outer_layout = QVBoxLayout(self.klar_page)
        klar_outer_layout.setAlignment(self.LAYOUT_STYLE['alignment'])
        klar_outer_layout.setSpacing(self.LAYOUT_STYLE['spacing'])
        klar_outer_layout.setContentsMargins(*self.LAYOUT_STYLE['margins'])
        
        klar_container = QWidget()
        klar_layout = QVBoxLayout(klar_container)
        klar_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        klar_outer_layout.addWidget(klar_container, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        klar_label = QLabel("KLAR Karteikartentrainer")
        klar_label.setAlignment(Qt.AlignCenter)
        klar_label.setStyleSheet(self.LAYOUT_STYLE['title_style'])
        klar_layout.addWidget(klar_label)
        
        # Zurück-Button mit zentraler Button-Funktion
        back_btn_klar = self.create_button(style="back")
        klar_layout.addWidget(back_btn_klar)

        
        # ------------------------------------
        # Modul-Liste für Reporting
        # ------------------------------------
        self.modules: list[TEACHModule] = []  # Wird später per register_module() gefüllt
        
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
        print_report_btn.clicked.connect(self.generate_pdf_report)
        status_btn.clicked.connect(lambda: (self.refresh_reports(), self.stack.setCurrentWidget(self.status_page)))
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

    # ------------------------------------------------------------
    # Reporting-Hilfsfunktionen
    # ------------------------------------------------------------
    def register_module(self, module: TEACHModule):
        """Registriert ein Modul für Reporting und andere Funktionen."""
        self.modules.append(module)

    def refresh_reports(self):
        """Aktualisiert die Report-Anzeige für alle registrierten Module."""
        container = QWidget()
        lay = QVBoxLayout(container)
        lay.setAlignment(Qt.AlignTop)
        lay.setSpacing(15)
        if not self.modules:
            lay.addWidget(QLabel("Keine Module registriert."))
        for mod in self.modules:
            try:
                data = mod.get_report()
            except Exception as exc:
                data = {"name": getattr(mod, "name", "Unbekannt"), "error": str(exc)}
            title = QLabel(f"Report: {data.get('name', 'Modul')}")
            title.setStyleSheet("font-weight: bold; font-size: 18px;")
            lay.addWidget(title)
            text = QTextEdit()
            text.setReadOnly(True)
            text.setPlainText(str(data))
            text.setFixedHeight(120)
            lay.addWidget(text)
        lay.addStretch(1)
        self.report_scroll.setWidget(container)

    def generate_pdf_report(self):
        """Erstellt einen PDF-Report aller Module und speichert ihn an einem vom Nutzer gewählten Ort."""
        if not self.modules:
            return  # Nichts zu drucken
        # Standarddateiname im Format DD-MM-YYYY_HH-MM_TEACH.pdf
        ts = datetime.now().strftime("%d-%m-%Y_%H-%M")
        default_name = f"{ts}_TEACH.pdf"
        path, _ = QFileDialog.getSaveFileName(self, "PDF speichern", default_name, "PDF Dateien (*.pdf)")
        if not path:
            return  # Abbruch
        writer = QPdfWriter(path)
        writer.setPageMargins(15, 15, 15, 15, QPageLayout.Millimeter)
        doc = QTextDocument()
        html_parts = []
        for mod in self.modules:
            try:
                data = mod.get_report()
            except Exception as exc:
                data = {"name": getattr(mod, "name", "Unbekannt"), "error": str(exc)}
            name = data.get("name", "Modul")
            details = json.dumps(data, indent=2, ensure_ascii=False)
            html_parts.append(f"<h2>{name}</h2><pre>{details}</pre>")
        doc.setHtml("\n".join(html_parts))
        doc.print(writer)
