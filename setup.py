# setup.py – Installation und Paketkonfiguration für T.E.A.C.H.
from setuptools import setup, find_packages  # Import von setuptools-Funktionen

setup(
    name="teach",  # Name des Pakets
    version="0.1.0",  # Version des Pakets
    description="T.E.A.C.H. Anwendung – Toll Ein Anderes Chaotisches Hilfeprogramm",  # kurze Beschreibung
    author="Unbekannt",  # Name des Autors
    packages=find_packages(where="src"),  # Alle Pakete unter src
    package_dir={"": "src"},  # Quellcode-Verzeichnis
    install_requires=[  # Abhängigkeiten
        "PySide6>=6.0.0",
    ],
    entry_points={  # Erzeugen eines GUI-Skripts
        "gui_scripts": [
            "teach=main:main",  # Befehl 'teach' startet die main()-Funktion in src/main.py
        ],
    },
)
