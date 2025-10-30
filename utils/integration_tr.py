# -*- coding: utf-8 -*-
"""
utils/integration_tr.py – Exportação/Importação do TR
Responsável por:
- Gravar o arquivo exports/tr_data.json a partir dos metadados do TR.
- Ler o arquivo exports/tr_data.json para pré-preencher o módulo Contrato.
"""

import json
import os
from typing import Dict, Any

EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
TR_JSON_PATH = os.path.join(EXPORTS_DIR, "tr_data.json")


def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    os.makedirs(path, exist_ok=True)


def export_tr_to_json(data: Dict[str, Any], path: str = TR_JSON_PATH) -> str:
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_tr_from_json(path: str = TR_JSON_PATH) -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}
