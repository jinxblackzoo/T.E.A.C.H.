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

### KI-Integration (geplant)
- Dynamische Modellverwaltung
- Kontextsensitive Hilfestellungen
- Dokumentenverarbeitung
- Anpassbare Lernniveaus

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

## 📝 Lizenz
[GNU GPL v3.0](LICENSE)

## 🤝 Mitwirken
Beiträge sind willkommen! Bitte lesen Sie unsere [Beitragsrichtlinien](CONTRIBUTING.md), bevor Sie Änderungen vornehmen.

## 📬 Kontakt
Bei Fragen oder Anregungen öffnen Sie bitte ein [Issue](https://github.com/jinxblackzoo/T.E.A.C.H./issues).
