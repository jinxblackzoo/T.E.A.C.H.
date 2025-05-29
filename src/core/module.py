from PySide6.QtWidgets import QWidget

class TEACHModule(QWidget):
    """Basisklasse für alle T.E.A.C.H. Module.
    
    Jedes Modul muss von dieser Klasse erben und die erforderlichen Methoden implementieren.
    """

    def get_report(self) -> dict:
        """
        Liefert einen Report als Dictionary mit den wichtigsten Status-/Fortschrittsdaten des Moduls.
        Muss von jedem Modul überschrieben werden.
        Rückgabeformat-Beispiel:
        {
            "name": "Modulname",
            "status": "OK",
            "details": {...}
        }
        """
        raise NotImplementedError("Das Modul muss die Methode get_report() implementieren.")
    
    def __init__(self, parent=None):
        """Initialisiert das Modul.
        
        Args:
            parent: Das übergeordnete Widget (normalerweise die Hauptanwendung)
        """
        super().__init__(parent)
        self.parent = parent
        self.name = "Unbenanntes Modul"
        self.description = "Keine Beschreibung verfügbar"
    
    def on_activate(self):
        """Wird aufgerufen, wenn das Modul aktiviert wird.
        
        Hier sollte die Hauptlogik des Moduls initialisiert werden.
        """
        pass
            
    def on_deactivate(self):
        """Wird aufgerufen, wenn das Modul deaktiviert wird.
        
        Hier sollten Ressourcen freigegeben und Aktionen zum Beenden durchgeführt werden.
        """
        pass
    
    def get_settings_widget(self):
        """Gibt ein Widget mit den Moduleinstellungen zurück.
        
        Returns:
            QWidget: Ein Widget mit den Einstellungen des Moduls
        """
        return QWidget()
    
    def save_settings(self):
        """Speichert die Moduleinstellungen.
        
        Diese Methode sollte überschrieben werden, um die Einstellungen zu speichern.
        """
        pass
    
    def load_settings(self):
        """Lädt die Moduleinstellungen.
        
        Diese Methode sollte überschrieben werden, um die Einstellungen zu laden.
        """
        pass
