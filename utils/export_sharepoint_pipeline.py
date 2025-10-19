# utils/export_sharepoint_pipeline.py
# ==============================================================
# SynapseNext – Fase Brasília (Passo 12A)
# Integração SharePoint e Flow Institucional – TJSP / SAAB
# ==============================================================

from datetime import datetime
from pathlib import Path
import json
import requests
import os

def publicar_sharepoint_relatorio(pdf_path: str, metadata: dict) -> dict:
    """
    Publica o relatório executivo no SharePoint institucional e registra log local.
    Retorna dict com status, URL e metadados.
    """
    # === Configurações básicas ===
    site_id = os.getenv("SHAREPOINT_SITE_ID", "tjsp-saab-site-id")
    drive_id = os.getenv("SHAREPOINT_DRIVE_ID", "RelatoriosSynapseNext")
    access_token = os.getenv("MS_GRAPH_TOKEN")  # obtido via MSAL / Flow

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/pdf"
    }

    file_name = Path(pdf_path).name
    upload_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{file_name}:/content"

    # === Upload do arquivo ===
    with open(pdf_path, "rb") as f:
        response = requests.put(upload_url, headers=headers, data=f)
    if response.status_code not in (200, 201):
        raise RuntimeError(f"Erro ao enviar arquivo: {response.status_code} – {response.text}")

    data = response.json()
    file_url = data.get("webUrl", "")
    version = metadata.get("version", "vNext")
    timestamp = datetime.utcnow().isoformat()

    # === Registro de log local ===
    log_entry = {
        "timestamp": timestamp,
        "file": file_name,
        "url": file_url,
        "status": "success",
        "metadata": metadata
    }
    log_dir = Path(__file__).resolve().parents[1] / "exports" / "auditoria"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "upload_log.jsonl"
    with open(log_path, "a", encoding="utf-8") as logf:
        logf.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    # === Retorno estruturado ===
    return {
        "status": "success",
        "file_url": file_url,
        "version": version,
        "uploaded_at": timestamp
    }
