# utils/integration_placeholders.py
# ==========================================================
# SynapseNext – Placeholders de integração institucional
# (Simula uploads e downloads para futura integração via Graph)
# ==========================================================

from datetime import datetime
from pathlib import Path
import json

def upload_to_sharepoint(filename: str, destination: str) -> dict:
    """
    Simula o upload de um arquivo para SharePoint.
    """
    return {
        "acao": "upload_sharepoint",
        "arquivo": filename,
        "destino": destination or "/sites/simulacao",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem": f"Arquivo '{filename}' simulado como enviado para '{destination or '/sites/simulacao'}'."
    }

def download_from_onedrive(filename: str) -> dict:
    """
    Simula o download de um arquivo a partir do OneDrive.
    """
    return {
        "acao": "download_onedrive",
        "arquivo": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mensagem": f"Arquivo '{filename}' simulado como baixado do OneDrive institucional."
    }

def save_integration_log(tipo: str, dados: dict):
    """
    Salva logs de integrações simuladas no diretório exports/logs.
    """
    base = Path(__file__).resolve().parents[1]
    logs_dir = base / "exports" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "tipo": tipo,
        "dados": dados,
    }

    log_path = logs_dir / f"integracao_{datetime.now().strftime('%Y%m%d')}.json"

    if log_path.exists():
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []

    logs.append(log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
