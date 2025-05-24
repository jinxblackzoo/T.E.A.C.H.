from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from .module import TEACHModule

class TEACH(QMainWindow):
    """Hauptfenster der T.E.A.C.H. Anwendung."""
    
    def __init__(self):
        """Initialisiert das Hauptfenster."""
        super().__init__()
        self.setWindowTitle("T.E.A.C.H. - Tolles Einfaches Adaptives Computer Hilfesystem")
        self.setGeometry(100, 100, 1024, 768)
        
        # Hauptwidget und Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Willkommensnachricht
        welcome_label = QLabel("Willkommen bei T.E.A.C.H.")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        self.layout.addWidget(welcome_label)
        
        # Status-Label
        self.status_label = QLabel("Lade Module...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)
        
        # Module laden
        self.modules = {}
        self.load_modules()
    
    def load_modules(self):
        """Lädt die verfügbaren Module dynamisch."""
        self.status_label.setText("Module geladen: Noch keine Module implementiert")
        # Hier werden später Module dynamisch geladen

    def activate_module(self, module_name):
        """Aktiviert ein Modul.
        
        Args:
            module_name (str): Name des zu aktivierenden Moduls
        """
        if module_name in self.modules:
            self.modules[module_name].on_activate()
            
    def deactivate_module(self, module_name):
        """Deaktiviert ein Modul.
        
        Args:
            module_name (str): Name des zu deaktivierenden Moduls
        """
        if module_name in self.modules:
            self.modules[module_name].on_deactivate()
