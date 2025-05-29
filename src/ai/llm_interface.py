"""llm_interface.py – Zentrale Schnittstelle zwischen T.E.A.C.H. und einem lokal laufenden LLM-Server.

Dieses Modul kapselt sämtliche HTTP-Aufrufe an die KI.  Dadurch:
1. Benötigt jedes Modul nur *eine* Funktion (`ask_llm`).
2. Ein späterer Modell- oder Serverwechsel erfordert nur Änderungen *hier*.
3. Einheitliche Fehlerbehandlung und Logging an einer Stelle.

Das Standard-End-Point und weitere Parameter (Modellname, Zeit-Out …) können
bei Bedarf angepasst oder per ENV-Variablen überschrieben werden.
"""

# -----------------------------------------------------------------------------
# Standard-Bibliotheken
# -----------------------------------------------------------------------------
from __future__ import annotations

import json  # Debug-/Fallback-Ausgabe als JSON
import os
import logging
from typing import Any, Dict

# -----------------------------------------------------------------------------
# Drittanbieter-Bibliotheken
# -----------------------------------------------------------------------------
import requests  # Für HTTP-POST zur LLM-API

# -----------------------------------------------------------------------------
# Konfigurierbare Konstanten  –  können via ENV überschrieben werden
# -----------------------------------------------------------------------------
L3_DEFAULT_API_URL = os.getenv("TEACH_LLM_API_URL", "http://localhost:4891/v1/chat/completions")
L3_DEFAULT_MODEL   = os.getenv("TEACH_LLM_MODEL", "ggml-model")
L3_DEFAULT_TIMEOUT = float(os.getenv("TEACH_LLM_TIMEOUT", "60"))  # Sekunden

# -----------------------------------------------------------------------------
# Öffentliche Hauptfunktion
# -----------------------------------------------------------------------------

def ask_llm(prompt: str,
            *,
            api_url: str = L3_DEFAULT_API_URL,
            model: str   = L3_DEFAULT_MODEL,
            max_tokens: int = 256,
            temperature: float = 0.7,
            **extra: Any) -> Dict[str, Any]:
    """Sendet *prompt* an das LLM-Server-End-Point und gibt strukturierte Antwort.

    Args:
        prompt:  Der vom Modul erzeugte Prompt.
        api_url: Basis-URL des LLM-Servers (inklusive Pfad).  Kann pro Aufruf
                  überschrieben werden.
        model:   Modell-Bezeichner gem. Server-Konfiguration.
        max_tokens: Maximale Tokenzahl der Antwort.
        temperature: Kreativitäts-Parameter (0–2).
        **extra:  Weitere Parameter, die ungeprüft an das JSON-Payload angehängt
                   werden (z.B. *top_p*, *stop* …).

    Returns:
        dict  –   Schlüsselfelder:
            "success" -> bool             Erfolg der Anfrage
            "text"    -> str | None       Antwort-Text (bei Erfolg)
            "error"   -> str | None       Fehlermeldung (bei Misserfolg)
    """
    # ----------------------- Payload vorbereiten -----------------------------
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        **extra,  # ermöglicht flexible Erweiterung
    }

    logging.debug("LLM-Request an %s mit Payload: %s", api_url, json.dumps(payload)[:500])

    # ----------------------- HTTP-POST ausführen ----------------------------
    try:
        resp = requests.post(api_url, json=payload, timeout=L3_DEFAULT_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        answer_txt = (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
        )
        return {"success": True, "text": answer_txt}

    except requests.RequestException as exc:
        logging.error("GPT4All-API-Fehler: %s", exc)
        return {"success": False, "error": str(exc)}

    except (ValueError, KeyError) as exc:  # JSON-Parsing oder Strukturfehler
        logging.error("Unerwartetes API-Antwortformat: %s", exc)
        return {"success": False, "error": f"Antwortformat-Fehler: {exc}"}
