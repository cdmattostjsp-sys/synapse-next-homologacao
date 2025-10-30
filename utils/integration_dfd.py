# -*- coding: utf-8 -*-
"""
utils/integration_dfd.py – Exportação/Importação do DFD para integração com ETP

Responsável por:
- Gravar o arquivo exports/dfd_data.json a partir dos metadados do DFD.
- Ler o arquivo exports/dfd_data.json para pré-preencher o módulo ETP.
- Funções simples, sem dependência de Streamlit, para facilitar testes unitários.
"""

from __future__ import annotations
import json
import os
from typing import Dict, Any

# Caminhos de exportação padrão
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
DFD_JSON_PATH = os.path.join(EXPORTS_DIR, "dfd_data.json")


def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    """Garante que o diretório de exportação exista."""
    os.makedirs(path, exist_ok=True)


def export_dfd_to_json(data: Dict[str, Any], path: str = DFD_JSON_PATH) -> str:
    """Salva metadados do DFD (dict) em JSON UTF-8. Retorna o caminho salvo."""
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_dfd_from_json(path: str = DFD_JSON_PATH) -> Dict[str, Any]:
    """Lê o arquivo JSON se existir; caso contrário, retorna {}."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}
