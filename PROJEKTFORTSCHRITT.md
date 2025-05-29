# 📅 Projektfortschritt

## 📌 Aktueller Status
- **GUI Framework**: PySide6 (Qt for Python)
- **Zielplattformen**: Windows, Linux, macOS
- **Datenbank**: SQLite pro Modul
- **Build-System**: PyInstaller

## ✅ Abgeschlossen
- [x] Projektkonzept erstellen
- [x] Technologie-Stack festlegen
- [x] Grundlegende Dokumentation
- [x] Verzeichnisstruktur anlegen
- [x] Kernklassen und Programmstruktur (App, Module, Manager) in Mindmaps festgelegt
- [x] Mindmap-Bereinigung (Kompatibilität Freeplane/Freemind)

## 🔄 In Arbeit
- [x] Hauptfenster und Navigation implementieren
- [x] Modul-Schnittstellen und Basisklassen finalisieren
- [ ] VOLL Vokabeltrainer-Modul entwickeln
- [ ] MUT Einheitentrainer-Modul entwickeln
- [ ] KLAR Karteikartentrainer-Modul entwickeln
- [ ] Dokumentation vervollständigen
- [ ] UI/UX optimieren
- [ ] KI-Schnittstelle in alle Module integrieren
- [ ] Konfigurierbarkeit verschiedener LLM-Backends
- [ ] Einheitliche Fehler- und Ausfallbehandlung
- [ ] Option zur KI-Deaktivierung in den Einstellungen
- [ ] Entwickler- und Nutzer-Dokumentation zur KI
- [ ] Erweiterte Analyse- und Lernfortschrittsfunktionen



## Modul VOLL

## Modul MUT

## Modul KLAR



## 🤖 KI-Integration
### Implementierte Funktionen
- [x] Zentrale LLM-Schnittstelle
- [x] Unterstützung für lokale KI-Modelle
- [x] Pädagogische Steuerung über Prompts
- [x] Fehlerbehandlung

### In Entwicklung
- [ ] Verbesserte Lernfortschrittsanalyse
- [ ] Anpassbare Lernpfade
- [ ] Erweiterte KI-Interaktionen

## 🏗️ Architektur-Entscheidungen

### Reporting Funktion
- Schnittstelle von TEACH zu jedem Modul
- Was reportet wird, wird im Modul festgelegt - TEACH soll nur anzeigen und als PDF speichern können
- UI Navigation: Reporting - Report als PDF drucken <-> Klick soll PDF-Report für alle Module erzeugen wie unter "Status anzeigen"
                           - Status anzeigen <-> Klick zeigt Seite mit den Reportparametern je nach Modul sortiert nach Modul

### Modul-System
- Jedes Modul ist ein eigenes Python-Paket
- Dynamisches Laden zur Laufzeit
- Klare Schnittstellen für Konfiguration, Datenzugriff und UI
- Schnittstelle zur Reporting Funktion
- Eigene Regelerstellung für die KI Nutzung (im Code, nicht veränderbar vom Nutzer im Programm)
- Modul muss auch ohne KI und offline funktionieren


### Datenhaltung
- **Pro Modul eine SQLite-Datei**
  - Vorteile: Einfache Migration, klare Trennung, einfache Backups
  - Nachteile: Keine übergreifenden Abfragen

### UI/UX
- Hauptmenü mit Modulauswahl
- Einheitliches Design-System
- Responsive Layouts
- Dunkel/Hell-Modus
