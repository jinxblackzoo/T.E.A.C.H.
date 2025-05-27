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
- [ ] Hauptfenster und Navigation (TEACH, ohne Module) implementieren
- [ ] Modul-Schnittstellen und Basisklassen finalisieren
- [ ] Module Schritt für Schritt einbinden
- [ ] Beispielmodul anlegen und testen
- [ ] Automatisierte Tests für Kernlogik
- [ ] Technische Dokumentation vervollständigen
- [ ] UI/UX-Design abstimmen
- [ ] README und Entwicklerdokumentation aktualisieren

## 🤖 KI-Integration

### Kernfunktionen
1. **Dynamische Modellverwaltung**
   - Austauschbare KI-Modelle (z.B. GPT, LLaMA, etc.)
   - Plugin-System für Modell-Adapter
   - Versionierung und Updates von Modellen

2. **Nachhilfe- & Erklärfunktion**
   - Kontextsensitive Hilfestellungen
   - Regelsystem zur Steuerung der Antworten
   - Anpassbare Lernniveaus

3. **Dokumentenverarbeitung**
   - PDF-Import mit Textextraktion
   - Erstellung von Lerninhalten
   - Wissensdatenbank

4. **Zahlungsintegration**
   - API-Schnittstelle für kostenpflichtige Modelle
   - Abrechnungssystem
   - Nutzungsüberwachung

## 🏗️ Architektur-Entscheidungen
### Modul-System
- Jedes Modul ist ein eigenes Python-Paket
- Dynamisches Laden zur Laufzeit
- Klare Schnittstellen für Konfiguration, Datenzugriff und UI

### Datenhaltung
- **Pro Modul eine SQLite-Datei**
  - Vorteile: Einfache Migration, klare Trennung, einfache Backups
  - Nachteile: Keine übergreifenden Abfragen

### UI/UX
- Hauptmenü mit Modulauswahl
- Einheitliches Design-System
- Responsive Layouts
- Dunkel/Hell-Modus
