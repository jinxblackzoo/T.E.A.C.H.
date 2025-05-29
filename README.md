# T.E.A.C.H.

Toll Ein Anderes Chaotisches Hilfeprogramm

## 📖 Überblick
T.E.A.C.H. ist eine modulare Lernplattform, die verschiedene Module unter einer einheitlichen Oberfläche vereint. Die Anwendung ist darauf ausgelegt, durch KI-Unterstützung ein personalisiertes Lernerlebnis zu bieten.

## 🎯 Ziele
- Einfache Integration verschiedener Lernmodule
- KI-gestützte Lernunterstützung
- Plattformübergreifende Verfügbarkeit
- Benutzerfreundliche Oberfläche
- Erweiterbarkeit durch Drittanbieter-Module

## 🛠 Technologie-Stack
- **GUI**: PySide6 (Qt for Python)
- **Datenbank**: SQLite pro Modul
- **Build-System**: PyInstaller
- **Zielplattformen**: Windows, Linux, macOS

## 🏗 Architektur
Die Anwendung folgt einem modularen Ansatz:
- **Kernsystem**: Verwaltet Module und stellt Basisfunktionalitäten bereit
- **Module**: Eigenständige Komponenten mit spezifischen Funktionen
- **Datenhaltung**: Jedes Modul verwaltet seine eigenen Daten in separaten SQLite-Datenbanken
- **Schnittstellen**: Klare APIs für die Kommunikation zwischen Modulen

## 📦 Module
### Kernmodule (geplant)
- **KLAR**: Künstliche Lern- und Arbeitsumgebung
- **VOLL**: Virtuelles Online-Lernlabor
- **MUT**: Modulares Unterrichts-Tool

## 🤖 KI-Integration

T.E.A.C.H. unterstützt die Verwendung lokaler KI-Modelle (z.B. GPT4All, Ollama) für intelligente Lernhilfen. Die KI-Funktionen sind optional und laufen komplett lokal auf Ihrem Rechner.

### Wichtige Informationen:
- **Lokale Ausführung**: Alle KI-Berechnungen finden auf Ihrem eigenen Gerät statt
- **Keine Cloud-Abhängigkeit**: Ihre Daten bleiben privat und werden nicht an Dritte gesendet
- **Flexible Modelle**: Nutzen Sie verschiedene Open-Source-Sprachmodelle
- **Pädagogische Steuerung**: Jedes Modul definiert eigene Regeln für die KI-Interaktion

### Voraussetzungen
- Ein laufender KI-Server (z.B. GPT4All Desktop, Ollama)
- Mindestens 8GB RAM empfohlen
- Internetverbindung nur zum Herunterladen der Modelle nötig

> **Hinweis**: Die Kernfunktionen von T.E.A.C.H. funktionieren auch ohne KI-Unterstützung.

## 🚀 Installation

### Voraussetzungen
- Python 3.9 oder höher
- pip (Python Paketmanager)

### Schritte
1. Repository klonen:
   ```bash
   git clone https://github.com/jinxblackzoo/T.E.A.C.H..git
   cd T.E.A.C.H.
   ```

2. Virtuelle Umgebung erstellen (empfohlen):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # ODER
   .\venv\Scripts\activate  # Windows
   ```

3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```

4. Anwendung starten:
   ```bash
   python src/main.py
   ```

### Windows
Der folgende Abschnitt zeigt, wie du T.E.A.C.H. unter Windows installierst und startest:
```powershell
# Repository klonen (in gewünschtes Verzeichnis)
PS> git clone https://github.com/jinxblackzoo/T.E.A.C.H. .
# Abhängigkeiten installieren
PS> pip install PySide6
# Anwendung starten
PS> python src/main.py
```

### Linux (ohne virtuelle Umgebung)
Der folgende Abschnitt zeigt, wie du T.E.A.C.H. unter Linux testest, ohne venv:
```bash
# Ins Projektverzeichnis wechseln
$ cd /Pfad/zum/Projekt
# Repository aktualisieren
$ git pull origin main
# Abhängigkeiten installieren
$ sudo pip3 install PySide6
# Anwendung starten
$ python3 src/main.py
```

### macOS
Der folgende Abschnitt zeigt, wie du T.E.A.C.H. unter macOS installierst und startest:
```bash
# Repository klonen (in gewünschtes Verzeichnis)
$ git clone https://github.com/jinxblackzoo/T.E.A.C.H. .
# Abhängigkeiten installieren
$ pip3 install PySide6
# Anwendung starten
$ python3 src/main.py
```

## 📝 Lizenz
[GNU GPL v3.0](LICENSE)

## 🤝 Mitwirken
Beiträge sind willkommen! Bitte lesen Sie unsere [Beitragsrichtlinien](CONTRIBUTING.md), bevor Sie Änderungen vornehmen.

## 📬 Kontakt
Bei Fragen oder Anregungen öffnen Sie bitte ein [Issue](https://github.com/jinxblackzoo/T.E.A.C.H./issues).
