# utils/auditoria_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 10A – Auditoria.IA)
# Trilhas auditáveis: hash digital, snapshots e JSONL por artefato
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib
import json
from typing import Any, Dict, Optional


# ----------------------------
# Utilitários internos
# ----------------------------
def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def _today_str() -> str:
    return datetime.now().strftime("%Y%m%d")

def _project_root() -> Path:
    # utils/auditoria_pipeline.py → raiz do projeto
    return Path(__file__).resolve().parents[1]

def _ensure_dirs() -> Dict[str, Path]:
    base = _project_root()
    dirs = {
        "auditoria": base / "exports" / "auditoria",
        "snapshots": base / "exports" / "auditoria" / "snapshots",
        "logs": base / "exports" / "logs",
    }
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    return dirs


# ----------------------------
# Funções públicas
# ----------------------------
def compute_sha256(text: str) -> str:
    """
    Calcula o hash SHA-256 de um texto (UTF-8).
    """
    if text is None:
        text = ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def audit_event(
    artefato: str,
    etapa: str,
    markdown_text: str,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Registra um evento de auditoria para um artefato (DFD, ETP, TR, Edital, etc.).

    - Gera hash SHA-256 do markdown
    - Salva snapshot do conteúdo em exports/auditoria/snapshots
    - Grava linha JSONL em exports/auditoria/audit_YYYYMMDD.jsonl
    - Acrescenta linha legível em exports/logs/audit_trail.txt

    Retorna um dicionário com informações do registro.
    """
    dirs = _ensure_dirs()

    timestamp = _now_iso()
    daytag = _today_str()
    text = markdown_text or ""
    sha256 = compute_sha256(text)

    # Estatísticas rápidas
    char_count = len(text)
    word_count = len(text.split()) if text.strip() else 0

    # Snapshot do markdown
    short_hash = sha256[:10]
    snap_name = f"{artefato}_{etapa}_{daytag}_{short_hash}.md"
    snap_path = dirs["snapshots"] / snap_name
    with open(snap_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Registro JSONL (um evento por linha)
    jsonl_path = dirs["auditoria"] / f"audit_{daytag}.jsonl"
    record = {
        "timestamp": timestamp,
        "artefato": artefato,
        "etapa": etapa,
        "sha256": sha256,
        "char_count": char_count,
        "word_count": word_count,
        "snapshot_relpath": str(snap_path.relative_to(_project_root())),
        "meta": meta or {},
    }
    with open(jsonl_path, "a", encoding="utf-8") as jf:
        jf.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Trilha legível
    trail_path = dirs["logs"] / "audit_trail.txt"
    with open(trail_path, "a", encoding="utf-8") as tf:
        tf.write(
            f"[{timestamp}] {artefato} | etapa={etapa} | hash={short_hash} "
            f"| words={word_count} | snap={record['snapshot_relpath']}\n"
        )

    return {
        "ok": True,
        "timestamp": timestamp,
        "artefato": artefato,
        "etapa": etapa,
        "sha256": sha256,
        "word_count": word_count,
        "char_count": char_count,
        "snapshot_path": str(snap_path),
        "jsonl_path": str(jsonl_path),
        "trail_path": str(trail_path),
    }


def read_last_audit(artefato: str) -> Optional[Dict[str, Any]]:
    """
    Retorna o último registro de auditoria (do dia corrente) para o artefato informado,
    caso exista; do contrário, None.
    """
    dirs = _ensure_dirs()
    jsonl_path = dirs["auditoria"] / f"audit_{_today_str()}.jsonl"
    if not jsonl_path.exists():
        return None

    last = None
    with open(jsonl_path, "r", encoding="utf-8") as jf:
        for line in jf:
            try:
                data = json.loads(line)
                if data.get("artefato") == artefato:
                    last = data
            except json.JSONDecodeError:
                continue
    return last
