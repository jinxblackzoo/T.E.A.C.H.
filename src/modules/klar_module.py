"""
KLARModule – Ein T.E.A.C.H.-Modul für Karteikartentraining
==========================================================
Dieses Modul integriert die Kernfunktionen des eigenständigen KLAR-Programms
in die T.E.A.C.H.-Umgebung. Der Fokus liegt auf den Grundfunktionen
(Karteikartenverwaltung, Lernmodus, Fortschrittsstatistiken) ohne die MUT-
Speziallogik.  Alle UI-Elemente werden mit PySide6 umgesetzt, um plattform-
übergreifende Kompatibilität zu gewährleisten.

Wichtige Hinweise:
• Dies ist eine erste, lauffähige Grundstruktur. Lern- und Editor-Ansichten
  sind zunächst Platzhalter und werden schrittweise erweitert.
• Die Klasse erbt von TEACHModule und implementiert die geforderten
  Schnittstellen (get_report, on_activate, …).
• Die Datenhaltung nutzt SQLAlchemy mit einer einzelnen SQLite-Datei pro
  Nutzer.  Das Datenverzeichnis wird – analog zu KLAR – im
  Benutzer-Konfigpfad (~/.local/share/teach/klar) angelegt.
• Die KI-Schnittstelle wird als Placeholder-Methode vorbereitet – eine
  spätere Implementierung kann dort Kartenvorschläge/Erklärungen erzeugen.
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
# Standardbibliotheken
import os  # Dateipfade & Verzeichnisse verwalten
import json  # (De-)Serialisierung von Keywords
from datetime import datetime  # Zeitstempel für Statistiken

# Drittanbieter: PySide6 für die Benutzeroberfläche
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PySide6.QtCore import Qt  # Layout-Konstanten

# Drittanbieter: SQLAlchemy für ORM-basierte Datenhaltung
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# TEACH-interne Basisklasse
from core.module import TEACHModule

# ---------------------------------------------------------------------------
# Datenbank-Setup
# ---------------------------------------------------------------------------
# 1. SQLAlchemy-Basisklasse erzeugen
Base = declarative_base()

# 2. Datenmodell definieren (vereinfachte Variante aus KLAR)
class Flashcard(Base):
    """ORM-Klasse für einzelne Karteikarten."""

    __tablename__ = "flashcards"

    # Primärschlüssel
    id: int = Column(Integer, primary_key=True)

    # Name der Datenbank (ermöglicht später mehrere Decks)
    database_name: str = Column(String, nullable=False)

    # Frage & Antworttext
    question: str = Column(String, nullable=False)
    answer: str = Column(String, nullable=False)

    # Keywords als JSON-Array (wird beim Setzen/Lesen konvertiert)
    keywords: str = Column(String, default="[]")

    # Lernstatistiken (vereinfachte Version)
    correct_count: int = Column(Integer, default=0)  # richtige Antworten (gesamt)
    wrong_count: int = Column(Integer, default=0)    # falsche Antworten (gesamt)
    level: int = Column(Integer, default=1)          # Lernstufe 1-4

    last_practiced: datetime = Column(DateTime)      # Letzter Übungszeitpunkt

    # Helfereigenschaft zum Arbeiten mit der JSON-Liste
    @property
    def keyword_list(self) -> list[str]:
        """Keywords als Python-Liste."""
        return json.loads(self.keywords or "[]")

    @keyword_list.setter
    def keyword_list(self, value: list[str]):
        if not isinstance(value, list):
            raise ValueError("Keywords müssen als Liste übergeben werden")
        self.keywords = json.dumps(value, ensure_ascii=False)

# ---------------------------------------------------------------------------
# Datenbank-Manager (minimal)
# ---------------------------------------------------------------------------
class KLARDBManager:
    """Verwaltet den Zugriff auf die SQLite-Datei für KLAR."""

    def __init__(self):
        # Basis-Verzeichnis unter XDG_DATA_HOME bzw. ~/.local/share
        data_home = os.environ.get(
            "XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
        self.data_dir = os.path.join(data_home, "teach", "klar")
        os.makedirs(self.data_dir, exist_ok=True)

        # Einzelne zentralisierte Datenbank-Datei (später evtl. mehrere Decks)
        self.db_path = os.path.join(self.data_dir, "klar.db")

        # Engine & SessionFactory anlegen
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    # ---------------------------------------------------------------------
    # API-Methoden
    # ---------------------------------------------------------------------
    def get_session(self) -> Session:
        """Erstellt eine neue SQLAlchemy-Session."""
        return self.SessionLocal()

    def get_stats(self) -> dict:
        """Aggregiert einfache Fortschritts-Statistiken für den Report."""
        session = self.get_session()
        try:
            total = session.query(Flashcard).count()
            mastered = session.query(Flashcard).filter(Flashcard.level == 4).count()
            in_progress = total - mastered
            mastery_rate = (mastered / total * 100) if total else 0
            return {
                "total_cards": total,
                "mastered": mastered,
                "in_progress": in_progress,
                "mastery_rate": round(mastery_rate, 2),
            }
        finally:
            session.close()

# Globale DB-Manager-Instanz für das Modul
_db_mgr = KLARDBManager()

# ---------------------------------------------------------------------------
# KLARModule – Hauptklasse
# ---------------------------------------------------------------------------
class KLARModule(TEACHModule):
    """Karteikarten-Modul als TEACH-Integration."""

    # ---------------------------------------------------------------------
    # Initialisierung & UI-Aufbau
    # ---------------------------------------------------------------------
    def __init__(self, parent=None):
        """Erstellt Grund-UI und initialisiert interne Strukturen."""
        super().__init__(parent)

        # Modulmetadaten (werden z.B. im Hauptmenü angezeigt)
        self.name = "KLAR – Karteikarten"
        self.description = (
            "Kinderfreundliches Karteikarten-Tool – integriert in T.E.A.C.H.")

        # Einfaches Layout: Überschrift + Platzhalter-Buttons
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.setSpacing(20)

        title_lbl = QLabel("KLAR – Karteikarten")
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_lbl)

        # Platzhalter-Button „Lernen starten“
        learn_btn = QPushButton("Lernen starten")
        learn_btn.clicked.connect(self._start_learning_placeholder)
        layout.addWidget(learn_btn)

        # Platzhalter-Button „Karten verwalten“
        manage_btn = QPushButton("Karten verwalten")
        manage_btn.clicked.connect(self._manage_cards_placeholder)
        layout.addWidget(manage_btn)

        layout.addStretch(1)  # Restliche Fläche auffüllen

    # ---------------------------------------------------------------------
    # Platzhalter-Callbacks – zeigen Hinweisfenster
    # ---------------------------------------------------------------------
    def _start_learning_placeholder(self):
        QMessageBox.information(
            self,
            "Noch nicht implementiert",
            "Der Lernmodus wird in einer späteren Version integriert.")

    def _manage_cards_placeholder(self):
        QMessageBox.information(
            self,
            "Noch nicht implementiert",
            "Die Kartenverwaltung wird in einer späteren Version integriert.")

    # ---------------------------------------------------------------------
    # TEACHModule-Schnittstellen
    # ---------------------------------------------------------------------
    def on_activate(self):
        """Wird beim Aktivieren des Moduls aufgerufen (derzeit keine Aktion)."""
        pass

    def on_deactivate(self):
        """Wird beim Deaktivieren des Moduls aufgerufen (derzeit keine Aktion)."""
        pass

    def get_report(self) -> dict:
        """Liefert einen Fortschritts-Report für das zentrale Reporting."""
        stats = _db_mgr.get_stats()
        return {
            "name": self.name,
            "status": "OK" if stats["total_cards"] > 0 else "Keine Karten",
            "details": stats,
        }

    # ---------------------------------------------------------------------
    # KI-Schnittstelle (Placeholder)
    # ---------------------------------------------------------------------
    def generate_ai_hint(self, question: str) -> str:
        """Vorbereitete Methode für KI-gestützte Hinweise.

        Diese Funktion kann später die zentrale LLM-API von TEACH nutzen, um
        Erklärungen oder Eselsbrücken zu generieren.  Aktuell wird nur ein
        Platzhalter zurückgegeben.
        """
        return "[KI-Hinweis noch nicht implementiert]"

# ---------------------------------------------------------------------------
# Hilfsfunktion zum Registrieren des Moduls in der Hauptanwendung
# ---------------------------------------------------------------------------

def register(app_window):
    """Erzeugt eine Instanz von KLARModule und meldet sie bei TEACH an."""
    module = KLARModule(parent=app_window)
    app_window.register_module(module)

