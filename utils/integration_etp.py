# -*- coding: utf-8 -*-
"""
utils/integration_etp.py – Exportação/Importação do ETP
Responsável por:
- Gravar o arquivo exports/etp_data.json a partir dos metadados do ETP.
- Ler o arquivo exports/etp_data.json para pré-preencher o módulo TR.
"""

import json
import os
from typing import Dict, Any

EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
ETP_JSON_PATH = os.path.join(EXPORTS_DIR, "etp_data.json")


def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    os.makedirs(path, exist_ok=True)


def export_etp_to_json(data: Dict[str, Any], path: str = ETP_JSON_PATH) -> str:
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_etp_from_json(path: str = ETP_JSON_PATH) -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}
