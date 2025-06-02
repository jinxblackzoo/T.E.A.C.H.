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
import random  # Karten mischen
import time  # Sitzungsdauer messen
from datetime import datetime  # Zeitstempel für Statistiken

# Drittanbieter: PySide6 für die Benutzeroberfläche
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QListWidget, QHBoxLayout, QInputDialog,
    QLineEdit, QTextEdit, QFileDialog, QStackedWidget
)
from PySide6.QtCore import Qt  # Layout-Konstanten
from PySide6.QtGui import QPixmap  # Bilder anzeigen

# Drittanbieter: SQLAlchemy für ORM-basierte Datenhaltung
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# TEACH-interne Basisklasse
from core.module import TEACHModule

# Zentrale LLM-Schnittstelle von T.E.A.C.H.
from ai.llm_interface import ask_llm

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

    # Optionaler Bildpfad (kann leer sein)
    image_path: str = Column(String, nullable=True)

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
# Zusätzliche ORM-Modelle
# ---------------------------------------------------------------------------

class StudySession(Base):
    """Speichert Informationen zu einer abgeschlossenen Lernsession."""

    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now)
    duration = Column(Float)  # Dauer in Sekunden
    cards_practiced = Column(Integer)
    correct_answers = Column(Integer)


class PracticeAttempt(Base):
    """Einzelversuch an einer Karteikarte (für detaillierte Statistik)."""

    __tablename__ = "practice_attempts"

    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    correct = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False)
    duration = Column(Integer, default=0)  # Dauer in Sekunden


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

        # Datei, in der der Name der aktiven Datenbank persistiert wird
        self.active_db_file = os.path.join(self.data_dir, ".active_db")

        # Aktive DB bestimmen bzw. auf Standard zurückfallen
        if os.path.exists(self.active_db_file):
            with open(self.active_db_file, "r", encoding="utf-8") as fh:
                self.active_db = fh.read().strip() or "klar.db"
        else:
            self.active_db = "klar.db"

        # Pfad zur aktiven DB
        self.db_path = os.path.join(self.data_dir, self.active_db)

        # Engine & SessionFactory anlegen/aktualisieren
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        
        # Erst Tabellen erstellen, dann Migration ausführen
        Base.metadata.create_all(self.engine)
        self._migrate_database()
        
        self.SessionLocal = sessionmaker(bind=self.engine)

    def _migrate_database(self):
        """Führt notwendige Datenbank-Migrationen durch."""
        try:
            # Prüfe, ob image_path Spalte in flashcards Tabelle existiert
            with self.engine.connect() as conn:
                # Hole Tabellen-Info mit text() für Raw SQL
                result = conn.execute(text("PRAGMA table_info(flashcards)"))
                columns = [row[1] for row in result.fetchall()]
                
                # Füge fehlende Spalten hinzu
                if 'image_path' not in columns:
                    conn.execute(text("ALTER TABLE flashcards ADD COLUMN image_path TEXT"))
                    conn.commit()
                    print("Migration: image_path Spalte zur flashcards Tabelle hinzugefügt")
                
                # Weitere Migrationen können hier hinzugefügt werden
                if 'last_practiced' not in columns:
                    conn.execute(text("ALTER TABLE flashcards ADD COLUMN last_practiced DATETIME"))
                    conn.commit()
                    print("Migration: last_practiced Spalte zur flashcards Tabelle hinzugefügt")
                    
        except Exception as e:
            print(f"Warnung: Migration fehlgeschlagen: {e}")
            # Migration-Fehler nicht kritisch - Anwendung kann trotzdem starten

    # ---------------------------------------------------------------------
    # API-Methoden
    # ---------------------------------------------------------------------
    def get_session(self) -> Session:
        """Erstellt eine neue SQLAlchemy-Session."""
        return self.SessionLocal()

    def get_stats(self) -> dict:
        """Aggregiert Fortschritts-Statistiken effizient mittels Aggregat-Funktionen."""
        session = self.get_session()
        try:
            total = session.query(Flashcard).count()
            mastered = session.query(Flashcard).filter(Flashcard.level == 4).count()
            in_progress = total - mastered
            mastery_rate = (mastered / total * 100) if total else 0

            # Sessions-Statistik
            session_count = session.query(StudySession).count()
            last_session = (
                session.query(StudySession)
                .order_by(StudySession.date.desc())
                .first()
            )

            # Aggregierte Genauigkeit
            total_cards_practiced, total_correct = (
                session.query(
                    func.sum(StudySession.cards_practiced),
                    func.sum(StudySession.correct_answers),
                ).one()
            )
            total_cards_practiced = total_cards_practiced or 0
            total_correct = total_correct or 0
            avg_accuracy = (
                round(total_correct / total_cards_practiced * 100, 2)
                if total_cards_practiced else 0.0
            )

            return {
                "total_cards": total,
                "mastered": mastered,
                "in_progress": in_progress,
                "mastery_rate": round(mastery_rate, 2),
                "sessions": session_count,
                "last_session": last_session.date.strftime("%Y-%m-%d %H:%M") if last_session else None,
                "avg_accuracy": avg_accuracy,
            }
        finally:
            session.close()

    def get_available_databases(self) -> list[str]:
        """Liefert alle *.db-Dateien im Datenverzeichnis."""
        return sorted([f for f in os.listdir(self.data_dir) if f.endswith(".db")])

    def get_active_database(self) -> str | None:
        """Gibt den Namen der aktuell verwendeten Datenbank zurück."""
        return getattr(self, "active_db", None)

    def set_active_database(self, name: str):
        """Setzt die angegebene Datenbank als aktiv und initialisiert die Engine neu."""
        if name not in self.get_available_databases():
            raise FileNotFoundError(f"Datenbank {name} existiert nicht.")

        # Status persistieren
        with open(self.active_db_file, "w", encoding="utf-8") as fh:
            fh.write(name)

        self.active_db = name
        self.db_path = os.path.join(self.data_dir, self.active_db)
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_database(self, display_name: str, internal: str):
        """Erstellt eine neue Datenbankdatei (internal.db)."""
        filename = f"{internal}.db"
        new_db_path = os.path.join(self.data_dir, filename)
        if os.path.exists(new_db_path):
            raise FileExistsError(f"Datenbank {filename} existiert bereits.")

        new_engine = create_engine(f"sqlite:///{new_db_path}", echo=False)
        Base.metadata.create_all(new_engine)

        # Erste DB? Dann direkt aktivieren
        if len(self.get_available_databases()) == 1:
            self.set_active_database(filename)

    def delete_database(self, name: str):
        """Löscht die angegebene Datenbankdatei und aktualisiert die aktive DB falls nötig."""
        db_path = os.path.join(self.data_dir, name)
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Datenbank {name} existiert nicht.")

        os.remove(db_path)

        # War das die aktive? -> neue auswählen bzw. Standard anlegen
        if name == self.active_db:
            remaining = self.get_available_databases()
            if remaining:
                self.set_active_database(remaining[0])
            else:
                # Keine DB mehr vorhanden – Standard-DB neu anlegen
                self.create_database("Standard", "klar")

    # ------------------------------------------------------------------
    # API zum Erfassen von Sessions / Attempts
    # ------------------------------------------------------------------

    def add_study_session(self, duration: float, cards_practiced: int, correct: int):
        """Schreibt eine neue Lernsession in die DB."""
        sess = self.get_session()
        try:
            entry = StudySession(
                duration=duration,
                cards_practiced=cards_practiced,
                correct_answers=correct,
            )
            sess.add(entry)
            sess.commit()
        finally:
            sess.close()

    def add_practice_attempt(self, flashcard_id: int, correct: bool, level: int, duration: int = 0):
        """Speichert einen Übungsversuch für detaillierte Statistiken."""
        sess = self.get_session()
        try:
            attempt = PracticeAttempt(
                flashcard_id=flashcard_id,
                correct=correct,
                level=level,
                duration=duration,
            )
            sess.add(attempt)
            sess.commit()
        finally:
            sess.close()

    # ------------------------------------------------------------------
    # Lernen / Level-Update
    # ------------------------------------------------------------------

    def update_learning_result(self, card_id: int, correct: bool, level_before: int):
        """Aktualisiert Level & Statistik nach einer Antwort."""
        sess = self.get_session()
        try:
            card: Flashcard = sess.get(Flashcard, card_id)
            if correct:
                card.level = min(card.level + 1, 4)
                card.correct_count += 1
            else:
                card.level = 1
                card.wrong_count += 1
            card.last_practiced = datetime.now()
            sess.commit()

            # Attempt protokollieren
            self.add_practice_attempt(card_id, correct, card.level)
        finally:
            sess.close()

    # ------------------------------------------------------------------
    # Flashcard CRUD
    # ------------------------------------------------------------------

    def list_flashcards(self):
        sess = self.get_session()
        try:
            return sess.query(Flashcard).order_by(Flashcard.id).all()
        finally:
            sess.close()

    def create_flashcard(self, question: str, answer: str, keywords: list[str], image_path: str | None):
        sess = self.get_session()
        try:
            card = Flashcard(
                database_name="default",
                question=question,
                answer=answer,
                keywords=json.dumps(keywords, ensure_ascii=False),
                image_path=image_path,
            )
            sess.add(card)
            sess.commit()
        finally:
            sess.close()

    def update_flashcard(self, card: Flashcard, question: str, answer: str, keywords: list[str], image_path: str | None):
        sess = self.get_session()
        try:
            db_card = sess.get(Flashcard, card.id)
            db_card.question = question
            db_card.answer = answer
            db_card.keywords = json.dumps(keywords, ensure_ascii=False)
            db_card.image_path = image_path
            sess.commit()
        finally:
            sess.close()

    def delete_flashcard(self, card: Flashcard):
        sess = self.get_session()
        try:
            db_card = sess.get(Flashcard, card.id)
            sess.delete(db_card)
            sess.commit()
        finally:
            sess.close()

    def list_recent_sessions(self, limit: int = 20):
        """Gibt die letzten Lern-Sessions (neueste zuerst) zurück."""
        sess = self.get_session()
        try:
            return (
                sess.query(StudySession)
                .order_by(StudySession.date.desc())
                .limit(limit)
                .all()
            )
        finally:
            sess.close()

    def get_cards_for_learning(self):
        """Gibt alle Karten zurück, die noch nicht gemeistert sind (Level < 4)."""
        sess = self.get_session()
        try:
            return sess.query(Flashcard).filter(Flashcard.level < 4).all()
        finally:
            sess.close()


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
        # Modulinformationen setzen
        self.name = "KLAR"
        self.description = "Karteikartentrainer mit KI-Unterstützung"
        
        # Hauptfenster-Referenz für zentrale Styles und Button-Erstellung
        main_app = self.parentWidget()
        teach_style = getattr(main_app, "LAYOUT_STYLE", None)
        
        # Hauptlayout für das Modul
        main_layout = QVBoxLayout(self)
        if teach_style:
            main_layout.setAlignment(teach_style['alignment'])
            main_layout.setSpacing(teach_style['spacing'])
            main_layout.setContentsMargins(*teach_style['margins'])
        
        # Stacked Widget für verschiedene Ansichten
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        
        # Verschiedene Seiten erstellen
        self._create_main_page()
        self._create_db_manager_page()
        self._create_card_manager_page()
        self._create_learning_page()
        self._create_stats_page()
        
        # Starte mit Hauptseite
        self.stack.setCurrentWidget(self.main_page)
    
    def _create_main_page(self):
        """Erstellt die Hauptseite des KLAR-Moduls."""
        self.main_page = QWidget()
        layout = QVBoxLayout(self.main_page)
        
        # Zentrale Button-Erstellung verwenden
        main_app = self.parentWidget()
        create_btn = getattr(main_app, "create_button", QPushButton)
        
        # Titel
        title = QLabel("KLAR - Karteikartentrainer")
        title.setAlignment(Qt.AlignCenter)
        if hasattr(main_app, "LAYOUT_STYLE"):
            title.setStyleSheet(main_app.LAYOUT_STYLE['title_style'])
        layout.addWidget(title)
        
        # Buttons für verschiedene Funktionen
        learn_btn = create_btn("Lernen starten")
        learn_btn.clicked.connect(self._show_learning_page)
        layout.addWidget(learn_btn)
        
        db_btn = create_btn("Datenbanken verwalten")
        db_btn.clicked.connect(self._show_db_manager_page)
        layout.addWidget(db_btn)
        
        cards_btn = create_btn("Karten verwalten")
        cards_btn.clicked.connect(self._show_card_manager_page)
        layout.addWidget(cards_btn)
        
        stats_btn = create_btn("Statistiken")
        stats_btn.clicked.connect(self._show_stats_page)
        layout.addWidget(stats_btn)
    
    def _create_db_manager_page(self):
        """Erstellt die Datenbankverwaltungsseite."""
        self.db_manager_page = DatabaseManagerWidget(self)
        self.stack.addWidget(self.db_manager_page)
    
    def _create_card_manager_page(self):
        """Erstellt die Kartenverwaltungsseite."""
        self.card_manager_page = FlashcardManagerWidget(self)
        self.stack.addWidget(self.card_manager_page)
    
    def _create_learning_page(self):
        """Erstellt die Lernseite."""
        self.learning_page = LearningWidget(self)
        self.stack.addWidget(self.learning_page)
    
    def _create_stats_page(self):
        """Erstellt die Statistikseite."""
        self.stats_page = StatsWidget(self)
        self.stack.addWidget(self.stats_page)
    
    def _show_db_manager_page(self):
        """Zeigt die Datenbankverwaltungsseite."""
        self.stack.setCurrentWidget(self.db_manager_page)
        self.db_manager_page.refresh()
    
    def _show_card_manager_page(self):
        """Zeigt die Kartenverwaltungsseite."""
        self.stack.setCurrentWidget(self.card_manager_page)
        self.card_manager_page.refresh()
    
    def _show_learning_page(self):
        """Zeigt die Lernseite."""
        self.stack.setCurrentWidget(self.learning_page)
    
    def _show_stats_page(self):
        """Zeigt die Statistikseite."""
        self.stack.setCurrentWidget(self.stats_page)
        self.stats_page.refresh()
    
    def show_main_page(self):
        """Kehrt zur Hauptseite zurück."""
        self.stack.setCurrentWidget(self.main_page)
    
    def start_learning(self):
        """Startet eine Lernsession."""
        self._show_learning_page()

    # ---------------------------------------------------------------------
    # Datenbankverwaltung
    # ---------------------------------------------------------------------
    def open_db_manager(self):
        """Öffnet die Datenbankverwaltung."""
        self._show_db_manager_page()

    def open_card_manager(self):
        """Öffnet die Kartenverwaltung."""
        self._show_card_manager_page()

    def open_stats(self):
        """Öffnet die Statistiken."""
        self._show_stats_page()
    
    # -----------------------------------------------------------------
    # Reporting-Schnittstelle
    # -----------------------------------------------------------------
    def get_report(self) -> dict:
        """Gibt einen ausführlichen Report für das globale Reporting zurück."""
        stats = _db_mgr.get_stats()
        status = "OK" if stats["total_cards"] else "Keine Karten"
        return {
            "name": self.name,
            "status": status,
            "details": stats,
        }

    # -----------------------------------------------------------------
    # KI-Schnittstelle
    # -----------------------------------------------------------------

    def generate_ai_hint(self, question: str, answer: str | None = None) -> str:
        """Ruft die zentrale TEACH-LLM-API auf und liefert eine kindgerechte Erklärung.

        Args:
            question: Die Kartenfrage.
            answer:   Optional die richtige Antwort, falls bereits bekannt.

        Returns:
            str – Erklärung oder Fehlermeldung.
        """
        prompt = (
            "Erkläre kindgerecht die folgende Karteikartenfrage. "
            "Gib eine kurze Eselsbrücke oder einen Merksatz zurück.\n\n"
            f"Frage: {question}\n" + (f"Antwort: {answer}\n" if answer else "")
        )
        resp = ask_llm(prompt, max_tokens=80, temperature=0.5)
        if resp.get("success"):
            return resp.get("text", "[Leere Antwort]").strip()
        return f"[LLM-Fehler: {resp.get('error')}]"


# ---------------------------------------------------------------------------
# Datenbankverwaltungs-Widget
# ---------------------------------------------------------------------------
class DatabaseManagerWidget(QWidget):
    """Widget zum Verwalten von Datenbanken."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.parent_mod = parent

        # Hauptlayout
        vbox = QVBoxLayout(self)
        
        # Titel
        title = QLabel("Datenbanken verwalten")
        title.setAlignment(Qt.AlignCenter)
        if hasattr(parent.parentWidget(), "LAYOUT_STYLE"):
            title.setStyleSheet(parent.parentWidget().LAYOUT_STYLE['title_style'])
        vbox.addWidget(title)

        # Liste der verfügbaren Datenbanken
        self.db_list = QListWidget()
        vbox.addWidget(self.db_list)

        # Buttons
        btn_layout = QHBoxLayout()
        
        # Zentrale Button-Erstellung verwenden
        create_btn = getattr(parent.parentWidget(), "create_button", QPushButton)
        
        new_btn = create_btn("Neue DB")
        new_btn.clicked.connect(self._create_db)
        btn_layout.addWidget(new_btn)

        select_btn = create_btn("Auswählen")
        select_btn.clicked.connect(self._select_db)
        btn_layout.addWidget(select_btn)

        delete_btn = create_btn("Löschen")
        delete_btn.clicked.connect(self._delete_db)
        btn_layout.addWidget(delete_btn)

        vbox.addLayout(btn_layout)
        
        # Zurück-Button
        back_btn = create_btn("← Zurück", "back")
        back_btn.clicked.connect(self.parent_mod.show_main_page)
        vbox.addWidget(back_btn)

        self._refresh_list()

    # -----------------------------------------------------------------
    # Interne Helper
    # -----------------------------------------------------------------
    def _refresh_list(self):
        """Aktualisiert die Anzeige der Datenbanken."""
        self.db_list.clear()
        for db_name in _db_mgr.get_available_databases():
            self.db_list.addItem(db_name)
        # Aktive DB selektieren
        active = _db_mgr.get_active_database()
        if active:
            items = self.db_list.findItems(active, Qt.MatchExactly)
            if items:
                self.db_list.setCurrentItem(items[0])

    def _select_db(self):
        item = self.db_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Datenbank wählen.")
            return
        try:
            _db_mgr.set_active_database(item.text())
            QMessageBox.information(self, "Aktualisiert", f"{item.text()} ist jetzt aktiv.")
            self._refresh_list()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", str(exc))

    def _create_db(self):
        name, ok = QInputDialog.getText(self, "Neue Datenbank", "Name der Datenbank:")
        if not ok or not name:
            return
        try:
            internal = name.lower().replace(" ", "_")
            _db_mgr.create_database(name, internal)
            QMessageBox.information(self, "Erstellt", f"Datenbank {name} wurde angelegt.")
            self._refresh_list()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", str(exc))

    def _delete_db(self):
        item = self.db_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Datenbank wählen.")
            return
        reply = QMessageBox.question(self, "Löschen?", f"{item.text()} wirklich löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                _db_mgr.delete_database(item.text())
                self._refresh_list()
            except Exception as exc:
                QMessageBox.critical(self, "Fehler", str(exc))

    def refresh(self):
        """Aktualisiert die Datenbankliste."""
        self._refresh_list()


# ---------------------------------------------------------------------------
# Kartenverwaltungs-Widget
# ---------------------------------------------------------------------------
class FlashcardManagerWidget(QWidget):
    """Widget zum Verwalten von Karten."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.parent_mod = parent

        vbox = QVBoxLayout(self)
        
        # Titel
        title = QLabel("Karten verwalten")
        title.setAlignment(Qt.AlignCenter)
        if hasattr(parent.parentWidget(), "LAYOUT_STYLE"):
            title.setStyleSheet(parent.parentWidget().LAYOUT_STYLE['title_style'])
        vbox.addWidget(title)

        # Liste der Karten
        self.card_list = QListWidget()
        vbox.addWidget(self.card_list)

        # Buttons
        btn_layout = QHBoxLayout()
        
        # Zentrale Button-Erstellung verwenden
        create_btn = getattr(parent.parentWidget(), "create_button", QPushButton)
        
        add_btn = create_btn("Hinzufügen")
        add_btn.clicked.connect(self._add)
        btn_layout.addWidget(add_btn)

        edit_btn = create_btn("Bearbeiten")
        edit_btn.clicked.connect(self._edit)
        btn_layout.addWidget(edit_btn)

        delete_btn = create_btn("Löschen")
        delete_btn.clicked.connect(self._delete)
        btn_layout.addWidget(delete_btn)

        vbox.addLayout(btn_layout)
        
        # Zurück-Button
        back_btn = create_btn("← Zurück", "back")
        back_btn.clicked.connect(self.parent_mod.show_main_page)
        vbox.addWidget(back_btn)

        self._refresh()

    # ----------------------------- Helper ---------------------------------
    def _refresh(self):
        self.card_list.clear()
        self.cards = _db_mgr.list_flashcards()
        for card in self.cards:
            self.card_list.addItem(f"{card.id}: {card.question}")

    def _get_current_card(self):
        idx = self.card_list.currentRow()
        if idx < 0:
            return None
        return self.cards[idx]

    # --------------------------- Slots -----------------------------------
    def _add(self):
        self.editor = FlashcardEditorWidget(self)
        self.editor.show()

    def _edit(self):
        card = self._get_current_card()
        if not card:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Karte wählen.")
            return
        self.editor = FlashcardEditorWidget(self, card)
        self.editor.show()

    def _delete(self):
        card = self._get_current_card()
        if not card:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Karte wählen.")
            return
        reply = QMessageBox.question(self, "Löschen?", "Karte endgültig löschen?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            _db_mgr.delete_flashcard(card)
            self._refresh()

    def refresh(self):
        """Aktualisiert die Kartenliste."""
        self._refresh()


# ---------------------------------------------------------------------------
# Kartenbearbeitungs-Widget
# ---------------------------------------------------------------------------
class FlashcardEditorWidget(QWidget):
    """Widget zum Bearbeiten einer Karte."""

    def __init__(self, parent: QWidget, card: Flashcard | None = None):
        super().__init__(parent)
        self.card = card

        vbox = QVBoxLayout(self)
        
        # Titel
        title = QLabel("Karte bearbeiten" if card else "Neue Karte")
        title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(title)

        # Frage
        vbox.addWidget(QLabel("Frage:"))
        self.question_edit = QLineEdit()
        vbox.addWidget(self.question_edit)

        # Antwort
        vbox.addWidget(QLabel("Antwort:"))
        self.answer_edit = QTextEdit()
        vbox.addWidget(self.answer_edit)

        # Keywords
        vbox.addWidget(QLabel("Stichwörter (kommagetrennt):"))
        self.keyword_edit = QLineEdit()
        vbox.addWidget(self.keyword_edit)

        # Bildpfad
        vbox.addWidget(QLabel("Bildpfad (optional):"))
        img_layout = QHBoxLayout()
        self.image_path_edit = QLineEdit()
        img_layout.addWidget(self.image_path_edit)
        browse_btn = QPushButton("Durchsuchen")
        browse_btn.clicked.connect(self._browse_image)
        img_layout.addWidget(browse_btn)
        vbox.addLayout(img_layout)

        # Buttons
        btn_row = QHBoxLayout()
        ok_btn = QPushButton("Speichern")
        cancel_btn = QPushButton("Abbrechen")
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)
        vbox.addLayout(btn_row)

        ok_btn.clicked.connect(self._save)
        cancel_btn.clicked.connect(self.close)

        # Wenn Karte vorhanden, Felder füllen
        if card:
            self.question_edit.setText(card.question)
            self.answer_edit.setPlainText(card.answer)
            keywords = json.loads(card.keywords) if card.keywords else []
            self.keyword_edit.setText(", ".join(keywords))
            self.image_path_edit.setText(card.image_path or "")

        # Zurück-Button
        back_btn = QPushButton("← Zurück")
        back_btn.clicked.connect(self.close)
        vbox.addWidget(back_btn)

    # --------------------------- Helper -----------------------------------
    def _browse_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Bild auswählen", "", "Bilder (*.png *.jpg *.jpeg *.gif)")
        if file:
            self.image_path_edit.setText(file)

    def _save(self):
        keywords = [kw.strip() for kw in self.keyword_edit.text().split(",") if kw.strip()]
        if self.card:
            _db_mgr.update_flashcard(self.card, self.question_edit.text().strip(), self.answer_edit.toPlainText().strip(), keywords, self.image_path_edit.text().strip() or None)
        else:
            _db_mgr.create_flashcard(self.question_edit.text().strip(), self.answer_edit.toPlainText().strip(), keywords, self.image_path_edit.text().strip() or None)
        self.close()


# ---------------------------------------------------------------------------
# Lern-Widget
# ---------------------------------------------------------------------------
class LearningWidget(QWidget):
    """Lern-Widget mit Level-Logik."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.parent_mod = parent

        # Karten vorbereiten (alle noch nicht gemeisterten)
        self.cards = _db_mgr.get_cards_for_learning()
        if not self.cards:
            QMessageBox.information(self, "Keine Karten", "Keine Karten zum Lernen verfügbar.")
            return

        random.shuffle(self.cards)
        self.current_index = 0
        self.correct_count = 0
        self.session_start = time.time()

        vbox = QVBoxLayout(self)
        
        # Titel
        title = QLabel("Lernmodus")
        title.setAlignment(Qt.AlignCenter)
        if hasattr(parent.parentWidget(), "LAYOUT_STYLE"):
            title.setStyleSheet(parent.parentWidget().LAYOUT_STYLE['title_style'])
        vbox.addWidget(title)

        # Fortschritt
        self.progress_label = QLabel()
        vbox.addWidget(self.progress_label)

        # Frage
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        vbox.addWidget(self.question_label)

        # Antwort (zunächst versteckt)
        self.answer_label = QLabel()
        self.answer_label.setWordWrap(True)
        self.answer_label.hide()
        vbox.addWidget(self.answer_label)

        # Buttons
        btn_layout = QHBoxLayout()
        
        # Zentrale Button-Erstellung verwenden
        create_btn = getattr(parent.parentWidget(), "create_button", QPushButton)
        
        self.show_answer_btn = create_btn("Antwort zeigen")
        self.show_answer_btn.clicked.connect(self._show_answer)
        btn_layout.addWidget(self.show_answer_btn)

        self.hint_btn = create_btn("Tipp")
        self.hint_btn.clicked.connect(self._show_hint)
        self.hint_btn.setEnabled(False)
        btn_layout.addWidget(self.hint_btn)

        vbox.addLayout(btn_layout)

        # Bewertungsbuttons (zunächst versteckt)
        self.rating_layout = QHBoxLayout()
        self.correct_btn = create_btn("Richtig")
        self.correct_btn.clicked.connect(lambda: self._rate_answer(True))
        self.rating_layout.addWidget(self.correct_btn)

        self.wrong_btn = create_btn("Falsch")
        self.wrong_btn.clicked.connect(lambda: self._rate_answer(False))
        self.rating_layout.addWidget(self.wrong_btn)

        vbox.addLayout(self.rating_layout)
        self._hide_rating_buttons()
        
        # Zurück-Button
        back_btn = create_btn("← Zurück", "back")
        back_btn.clicked.connect(self.parent_mod.show_main_page)
        vbox.addWidget(back_btn)

        self._show_current_card()

    def _show_current_card(self):
        """Zeigt die aktuelle Karte an."""
        if self.current_index >= len(self.cards):
            self._finish_session()
            return
            
        card = self.cards[self.current_index]
        self.progress_label.setText(f"Karte {self.current_index + 1} von {len(self.cards)}")
        self.question_label.setText(card.question)
        self.answer_label.setText(card.answer)
        self.answer_label.hide()
        self.show_answer_btn.show()
        self._hide_rating_buttons()
        self.hint_btn.setEnabled(True)

    def _show_answer(self):
        """Zeigt die Antwort zur aktuellen Karte."""
        self.answer_label.show()
        self.show_answer_btn.hide()
        self._show_rating_buttons()

    def _show_rating_buttons(self):
        """Zeigt die Bewertungsbuttons."""
        self.correct_btn.show()
        self.wrong_btn.show()

    def _hide_rating_buttons(self):
        """Versteckt die Bewertungsbuttons."""
        self.correct_btn.hide()
        self.wrong_btn.hide()

    def _rate_answer(self, correct: bool):
        """Bewertet die Antwort und geht zur nächsten Karte."""
        card = self.cards[self.current_index]
        if correct:
            self.correct_count += 1
            card.level = min(card.level + 1, 4)
        else:
            card.level = max(card.level - 1, 0)
        
        # Karte in Datenbank aktualisieren
        _db_mgr.update_learning_result(card.id, correct, card.level)
        
        self.current_index += 1
        self._show_current_card()

    def _show_hint(self):
        """Zeigt einen Tipp zur aktuellen Karte."""
        card = self.cards[self.current_index]
        if hasattr(card, 'keywords') and card.keywords:
            try:
                keywords = json.loads(card.keywords) if isinstance(card.keywords, str) else card.keywords
                if keywords:
                    hint_text = f"Tipp: {', '.join(keywords[:2])}"
                    QMessageBox.information(self, "Tipp", hint_text)
                else:
                    QMessageBox.information(self, "Tipp", "Keine Hinweise verfügbar.")
            except:
                QMessageBox.information(self, "Tipp", "Keine Hinweise verfügbar.")
        else:
            QMessageBox.information(self, "Tipp", "Keine Hinweise verfügbar.")

    def _finish_session(self):
        """Beendet die Lernsession."""
        duration = time.time() - self.session_start
        accuracy = (self.correct_count / len(self.cards)) * 100 if self.cards else 0
        
        # Session in Datenbank speichern
        _db_mgr.add_study_session(duration, len(self.cards), self.correct_count)
        
        QMessageBox.information(
            self, 
            "Session beendet", 
            f"Du hast {self.correct_count} von {len(self.cards)} Karten richtig beantwortet.\n"
            f"Genauigkeit: {accuracy:.1f}%\n"
            f"Dauer: {int(duration)} Sekunden"
        )
        
        self.parent_mod.show_main_page()


# ---------------------------------------------------------------------------
# Statistik-Widget
# ---------------------------------------------------------------------------
class StatsWidget(QWidget):
    """Widget für Statistiken."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.parent_mod = parent
        
        vbox = QVBoxLayout(self)
        
        # Titel
        title = QLabel("Statistiken")
        title.setAlignment(Qt.AlignCenter)
        if hasattr(parent.parentWidget(), "LAYOUT_STYLE"):
            title.setStyleSheet(parent.parentWidget().LAYOUT_STYLE['title_style'])
        vbox.addWidget(title)

        # Statistiken anzeigen
        self.stats_label = QLabel()
        vbox.addWidget(self.stats_label)

        vbox.addWidget(QLabel("Letzte Sessions:"))
        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)
        
        # Zurück-Button
        create_btn = getattr(parent.parentWidget(), "create_button", QPushButton)
        back_btn = create_btn("← Zurück", "back")
        back_btn.clicked.connect(self.parent_mod.show_main_page)
        vbox.addWidget(back_btn)

        self._load_stats()

    def _load_stats(self):
        """Lädt und zeigt die Statistiken."""
        stats = _db_mgr.get_stats()
        stats_text = f"Karten gesamt: {stats.get('total_cards', 0)}\n"
        stats_text += f"Gemeisterte Karten: {stats.get('mastered_cards', 0)}\n"
        stats_text += f"Lernsessions: {stats.get('total_sessions', 0)}"
        
        self.stats_label.setText(stats_text)

        # Sessions laden
        self.list_widget.clear()
        for sess in _db_mgr.list_recent_sessions():
            duration = int(sess.duration) if sess.duration else 0
            self.list_widget.addItem(
                f"{sess.date.strftime('%Y-%m-%d %H:%M')} – "
                f"{sess.correct_answers}/{sess.cards_practiced} richtig, "
                f"{duration}s"
            )

    def refresh(self):
        """Aktualisiert die Statistiken."""
        self._load_stats()


# ---------------------------------------------------------------------------
# Hilfsfunktion zum Registrieren des Moduls in der Hauptanwendung
# ---------------------------------------------------------------------------

def register(app_window):
    """Erzeugt eine Instanz von KLARModule, meldet sie bei TEACH an und bettet das Widget in die KLAR-Seite ein."""
    module = KLARModule(parent=app_window)
    app_window.register_module(module)
    # Das KLARModule-Widget als Attribut speichern (optional, für späteren Zugriff)
    app_window.klar_modul_widget = module
    # In die KLAR-Seite einbetten
    # Annahme: klar_page enthält ein Layout mit mindestens einem Container (siehe app.py)
    # Wir suchen das zentrale Layout und fügen das Widget hinzu
    # (Das Widget wird nach dem Label und vor dem Zurück-Button eingefügt)
    for i in range(app_window.klar_page.layout().count()):
        item = app_window.klar_page.layout().itemAt(i)
        container = item.widget() if item else None
        # Wir suchen das zentrale Widget, das das Layout für KLAR enthält
        if container and isinstance(container, QWidget) and container.layout():
            # Das eigentliche Modul-Widget einfügen
            container.layout().insertWidget(1, module)  # Nach dem Label, vor dem Back-Button
            break
