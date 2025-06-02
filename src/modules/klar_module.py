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
    QLineEdit, QTextEdit, QFileDialog
)
from PySide6.QtCore import Qt  # Layout-Konstanten
from PySide6.QtGui import QPixmap  # Bilder anzeigen

# Drittanbieter: SQLAlchemy für ORM-basierte Datenhaltung
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, func
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
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

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
            "Karteikarten Lernen Aber Richtig – integriert in T.E.A.C.H.")

        # Einfaches Layout: Überschrift + Platzhalter-Buttons
        layout = QVBoxLayout(self)
        # Layout gemäß zentraler T.E.A.C.H.-Definition
        main_app = self.parentWidget()
        teach_style = getattr(main_app, "LAYOUT_STYLE", None)

        if teach_style:  # Falls vorhanden, Style-Werte übernehmen
            layout.setAlignment(teach_style.get("alignment", Qt.AlignTop | Qt.AlignHCenter))
            layout.setSpacing(teach_style.get("spacing", 20))
            # Innenabstände
            if "margins" in teach_style:
                layout.setContentsMargins(*teach_style["margins"])
        else:
            # Fallback auf Standardwerte
            layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
            layout.setSpacing(20)

        title_lbl = QLabel("KLAR – Karteikarten")
        # Titel-Style an zentrale Vorgabe anlehnen
        if teach_style and "title_style" in teach_style:
            title_lbl.setStyleSheet(teach_style["title_style"])
        else:
            title_lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_lbl)

        # Buttons – zentraler Helper sorgt für einheitliches Design
        create_btn = getattr(main_app, "create_button", QPushButton)

        # Platzhalter-Button „Lernen starten“
        learn_btn = create_btn("Lernen starten")
        learn_btn.clicked.connect(self.start_learning)
        layout.addWidget(learn_btn)

        # Datenbanken verwalten
        manage_btn = create_btn("Datenbanken verwalten")
        manage_btn.clicked.connect(self.open_db_manager)
        layout.addWidget(manage_btn)

        # Karten verwalten
        card_btn = create_btn("Karten verwalten")
        card_btn.clicked.connect(self.open_card_manager)
        layout.addWidget(card_btn)

        # Statistiken anzeigen
        stats_btn = create_btn("Statistiken")
        stats_btn.clicked.connect(self.open_stats)
        layout.addWidget(stats_btn)

        layout.addStretch(1)  # Restliche Fläche auffüllen

    # ---------------------------------------------------------------------
    # Lernmodus
    # ---------------------------------------------------------------------
    def start_learning(self):
        """Startet eine Lernsession im Dialog."""
        # Entferne Dialog und verwende Widget direkt im Hauptfenster
        pass  # TODO: Implementierung für Widget-basierte Lernsession

    # ---------------------------------------------------------------------
    # Datenbankverwaltung – Dialog öffnen
    # ---------------------------------------------------------------------
    def open_db_manager(self):
        """Öffnet den Dialog zum Verwalten der Karteikarten-Datenbanken."""
        # Entferne Dialog und verwende Widget direkt im Hauptfenster
        pass  # TODO: Implementierung für Widget-basierte Datenbankverwaltung

    def open_card_manager(self):
        """Öffnet den Karteneditor-Dialog."""
        # Entferne Dialog und verwende Widget direkt im Hauptfenster
        pass  # TODO: Implementierung für Widget-basierte Kartenverwaltung

    def open_stats(self):
        """Öffnet Statistik-Dialog."""
        # Entferne Dialog und verwende Widget direkt im Hauptfenster
        pass  # TODO: Implementierung für Widget-basierte Statistiken

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
# Dialogklasse für Datenbankverwaltung
# ---------------------------------------------------------------------------
class DatabaseManagerDialog(QWidget):
    """UI-Dialog zum Anlegen, Auswählen und Löschen von DBs."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.setWindowTitle("Datenbanken verwalten")
        self.resize(400, 300)

        self.parent_mod: KLARModule = parent

        # Hauptlayout
        vbox = QVBoxLayout(self)

        # Liste der vorhandenen Datenbanken
        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)

        # Buttons
        btn_row = QHBoxLayout()
        vbox.addLayout(btn_row)

        self.btn_set_active = QPushButton("Aktiv setzen")
        self.btn_new = QPushButton("Neu …")
        self.btn_delete = QPushButton("Löschen")
        btn_row.addWidget(self.btn_set_active)
        btn_row.addWidget(self.btn_new)
        btn_row.addWidget(self.btn_delete)

        # Signale
        self.btn_set_active.clicked.connect(self._set_active)
        self.btn_new.clicked.connect(self._create_new)
        self.btn_delete.clicked.connect(self._delete)

        # Liste initial füllen
        self._refresh_list()

    # -----------------------------------------------------------------
    # Interne Helper
    # -----------------------------------------------------------------
    def _refresh_list(self):
        """Aktualisiert die Anzeige der Datenbanken."""
        self.list_widget.clear()
        for db_name in _db_mgr.get_available_databases():
            self.list_widget.addItem(db_name)
        # Aktive DB selektieren
        active = _db_mgr.get_active_database()
        if active:
            items = self.list_widget.findItems(active, Qt.MatchExactly)
            if items:
                self.list_widget.setCurrentItem(items[0])

    def _set_active(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Datenbank wählen.")
            return
        try:
            _db_mgr.set_active_database(item.text())
            QMessageBox.information(self, "Aktualisiert", f"{item.text()} ist jetzt aktiv.")
            self._refresh_list()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", str(exc))

    def _create_new(self):
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

    def _delete(self):
        item = self.list_widget.currentItem()
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

    # ---------------------------------------------------------------------
    # TEACHModule-Schnittstellen
    # ---------------------------------------------------------------------
    def on_activate(self):
        """Wird beim Aktivieren des Moduls aufgerufen (derzeit keine Aktion)."""
        pass

    def on_deactivate(self):
        """Wird beim Deaktivieren des Moduls aufgerufen (derzeit keine Aktion)."""
        pass

    # ---------------------------------------------------------------------
    # KI-Schnittstelle-Methode wurde in KLARModule implementiert.
    # ---------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Dialogklasse für Kartenverwaltung
# ---------------------------------------------------------------------------
class FlashcardManagerDialog(QWidget):
    """Dialog zum Anlegen, Bearbeiten und Löschen von Flashcards."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.setWindowTitle("Karten verwalten")
        self.resize(500, 400)

        self.parent_mod: KLARModule = parent

        vbox = QVBoxLayout(self)

        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)

        btn_row = QHBoxLayout()
        vbox.addLayout(btn_row)

        self.btn_add = QPushButton("Neu …")
        self.btn_edit = QPushButton("Bearbeiten …")
        self.btn_delete = QPushButton("Löschen")
        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_edit)
        btn_row.addWidget(self.btn_delete)

        self.btn_add.clicked.connect(self._add)
        self.btn_edit.clicked.connect(self._edit)
        self.btn_delete.clicked.connect(self._delete)

        self._refresh()

    # ----------------------------- Helper ---------------------------------
    def _refresh(self):
        self.list_widget.clear()
        self.cards = _db_mgr.list_flashcards()
        for card in self.cards:
            self.list_widget.addItem(f"{card.id}: {card.question}")

    def _get_current_card(self):
        idx = self.list_widget.currentRow()
        if idx < 0:
            return None
        return self.cards[idx]

    # --------------------------- Slots -----------------------------------
    def _add(self):
        self.editor = FlashcardEditorDialog(self)
        self.editor.show()

    def _edit(self):
        card = self._get_current_card()
        if not card:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte eine Karte wählen.")
            return
        self.editor = FlashcardEditorDialog(self, card)
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


# ---------------------------------------------------------------------------
# Dialog zum Bearbeiten einer einzelnen Karte
# ---------------------------------------------------------------------------
class FlashcardEditorDialog(QWidget):
    """Dialog zum Hinzufügen oder Bearbeiten einer Karte."""

    def __init__(self, parent: QWidget, card: Flashcard | None = None):
        super().__init__(parent)
        self.setWindowTitle("Karte bearbeiten" if card else "Neue Karte")
        self.resize(500, 400)

        self.card = card

        vbox = QVBoxLayout(self)

        self.question_edit = QLineEdit()
        self.question_edit.setPlaceholderText("Frage")
        vbox.addWidget(self.question_edit)

        self.answer_edit = QTextEdit()
        self.answer_edit.setPlaceholderText("Antwort")
        vbox.addWidget(self.answer_edit)

        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText("Keywords (Komma getrennt)")
        vbox.addWidget(self.keyword_edit)

        img_row = QHBoxLayout()
        vbox.addLayout(img_row)
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setPlaceholderText("Bildpfad (optional)")
        img_row.addWidget(self.image_path_edit)
        browse_btn = QPushButton("Durchsuchen …")
        img_row.addWidget(browse_btn)

        browse_btn.clicked.connect(self._browse)

        # Buttons OK / Abbrechen
        btn_row = QHBoxLayout()
        vbox.addLayout(btn_row)
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Abbrechen")
        btn_row.addStretch(1)
        btn_row.addWidget(ok_btn)
        btn_row.addWidget(cancel_btn)

        ok_btn.clicked.connect(self._save)
        cancel_btn.clicked.connect(self.close)

        # Wenn Karte vorhanden, Felder füllen
        if card:
            self.question_edit.setText(card.question)
            self.answer_edit.setPlainText(card.answer)
            self.keyword_edit.setText(", ".join(card.keyword_list))
            if card.image_path:
                self.image_path_edit.setText(card.image_path)

    # --------------------------- Helper -----------------------------------
    def _browse(self):
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
# Dialog für Lernmodus
# ---------------------------------------------------------------------------
class LearningDialog(QWidget):
    """Einfacher Lern-Dialog mit Level-Logik."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.setWindowTitle("Lernmodus")
        self.resize(600, 400)

        self.parent_mod = parent

        # Karten vorbereiten (alle noch nicht gemeisterten)
        self.cards = [c for c in _db_mgr.list_flashcards() if c.level < 4]
        if not self.cards:
            QMessageBox.information(self, "Nichts zu lernen", "Es gibt keine fälligen Karten.")
            self.close()
            return
        random.shuffle(self.cards)
        self.current_idx = -1
        self.correct_count = 0

        self.start_time = time.time()

        # UI aufbauen
        vbox = QVBoxLayout(self)

        self.question_lbl = QLabel()
        self.question_lbl.setWordWrap(True)
        self.question_lbl.setStyleSheet("font-size:18px;font-weight:bold;")
        vbox.addWidget(self.question_lbl)

        self.image_lbl = QLabel()
        self.image_lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.image_lbl)

        self.answer_lbl = QLabel()
        self.answer_lbl.setWordWrap(True)
        self.answer_lbl.setVisible(False)
        vbox.addWidget(self.answer_lbl)

        btn_row = QHBoxLayout()
        vbox.addLayout(btn_row)

        self.reveal_btn = QPushButton("Antwort anzeigen")
        self.correct_btn = QPushButton("Richtig ✅")
        self.wrong_btn = QPushButton("Falsch ❌")

        btn_row.addWidget(self.reveal_btn)
        btn_row.addWidget(self.correct_btn)
        btn_row.addWidget(self.wrong_btn)

        self.correct_btn.setVisible(False)
        self.wrong_btn.setVisible(False)

        self.reveal_btn.clicked.connect(self._reveal)
        self.correct_btn.clicked.connect(lambda: self._answer(True))
        self.wrong_btn.clicked.connect(lambda: self._answer(False))

        # Tipp-Button
        self.hint_btn = QPushButton("Tipp 💡")
        btn_row.addWidget(self.hint_btn)
        self.hint_btn.clicked.connect(self._show_hint)

        # Label für KI-Hinweis
        self.hint_lbl = QLabel()
        self.hint_lbl.setWordWrap(True)
        self.hint_lbl.setStyleSheet("font-style: italic; color: #555;")
        self.hint_lbl.setVisible(False)
        vbox.addWidget(self.hint_lbl)

        # Erste Karte anzeigen
        self._next_card()

    # ----------------------------- Ablauf ---------------------------------
    def _next_card(self):
        self.current_idx += 1
        if self.current_idx >= len(self.cards):
            self._finish()
            return
        card = self.cards[self.current_idx]

        self.question_lbl.setText(card.question)
        self.answer_lbl.setText(card.answer)
        self.answer_lbl.setVisible(False)
        self.reveal_btn.setVisible(True)
        self.correct_btn.setVisible(False)
        self.wrong_btn.setVisible(False)
        self.hint_lbl.clear()
        self.hint_lbl.setVisible(False)
        self.hint_btn.setEnabled(True)

        # Bild
        if card.image_path and os.path.exists(card.image_path):
            pix = QPixmap(card.image_path)
            self.image_lbl.setPixmap(pix.scaledToWidth(300, Qt.SmoothTransformation))
            self.image_lbl.setVisible(True)
        else:
            self.image_lbl.clear()
            self.image_lbl.setVisible(False)

        # Tipp-Button erst nach 1 Sek. aktivieren, um versehentliches Klicken zu vermeiden
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.hint_btn.setEnabled(True))

    def _reveal(self):
        self.answer_lbl.setVisible(True)
        self.reveal_btn.setVisible(False)
        self.correct_btn.setVisible(True)
        self.wrong_btn.setVisible(True)

    def _answer(self, correct: bool):
        card = self.cards[self.current_idx]
        level_before = card.level
        _db_mgr.update_learning_result(card.id, correct, level_before)
        if correct:
            self.correct_count += 1
        self._next_card()

    def _finish(self):
        duration = time.time() - self.start_time
        _db_mgr.add_study_session(duration, len(self.cards), self.correct_count)
        QMessageBox.information(
            self,
            "Fertig",
            f"Session beendet. Richtig: {self.correct_count}/{len(self.cards)}")
        self.close()

    def _show_hint(self):
        """Fragt das LLM nach einem Tipp für die aktuelle Frage."""
        card = self.cards[self.current_idx]
        self.hint_btn.setEnabled(False)
        hint = self.parent_mod.generate_ai_hint(card.question)
        self.hint_lbl.setText(hint)
        self.hint_lbl.setVisible(True)


# ---------------------------------------------------------------------------
# Dialog für Statistiken
# ---------------------------------------------------------------------------
class StatsDialog(QWidget):
    """Zeigt aggregierte Lernstatistiken und Historie."""

    def __init__(self, parent: KLARModule):
        super().__init__(parent)
        self.setWindowTitle("Statistiken")
        self.resize(500, 400)

        vbox = QVBoxLayout(self)

        stats = _db_mgr.get_stats()
        vbox.addWidget(QLabel(f"Karten insgesamt: {stats['total_cards']}"))
        vbox.addWidget(QLabel(f"Gemeistert (Level 4): {stats['mastered']}"))
        vbox.addWidget(QLabel(f"In Bearbeitung: {stats['in_progress']}"))
        vbox.addWidget(QLabel(f"Meisterungsrate: {stats['mastery_rate']} %"))
        vbox.addWidget(QLabel(f"Anzahl der Lern-Sessions: {stats['sessions']}"))
        vbox.addWidget(QLabel(f"Letzte Lern-Session: {stats['last_session']}"))
        vbox.addWidget(QLabel(f"Durchschnittliche Genauigkeit: {stats['avg_accuracy']} %"))

        vbox.addWidget(QLabel("Letzte Lern-Sessions:"))
        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)

        for sess in _db_mgr.list_recent_sessions():
            duration = int(sess.duration) if sess.duration else 0
            self.list_widget.addItem(
                f"{sess.date.strftime('%Y-%m-%d %H:%M')} – "
                f"{sess.correct_answers}/{sess.cards_practiced} richtig, "
                f"{duration}s"
            )


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
