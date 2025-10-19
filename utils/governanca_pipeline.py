# utils/governanca_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 11A – Painel de Governança)
# Lê históricos de:
#  - Auditoria.IA  → exports/auditoria/audit_*.jsonl
#  - Comparador.IA → exports/analises/relatorio_coerencia_*.json
# Consolida métricas e prepara dados para o painel Streamlit.
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import re

# ----------------------------------------------------------
# Caminhos
# ----------------------------------------------------------
def _root() -> Path:
    return Path(__file__).resolve().parents[1]

def _dir_auditoria() -> Path:
    return _root() / "exports" / "auditoria"

def _dir_analises() -> Path:
    return _root() / "exports" / "analises"

# ----------------------------------------------------------
# Utilitários (datas e parsing)
# ----------------------------------------------------------
_dt_jsonl_name = re.compile(r"audit_(\d{8})\.jsonl$")
_dt_relatorio_name = re.compile(r"relatorio_coerencia_(\d{8})_\d{6}\.json$")

def _parse_daytag_from_jsonl(path: Path) -> Optional[str]:
    m = _dt_jsonl_name.search(path.name)
    return m.group(1) if m else None

def _parse_stamp_from_relatorio(path: Path) -> Optional[str]:
    # Formato: relatorio_coerencia_YYYYMMDD_HHMMSS.json
    m = _dt_relatorio_name.search(path.name)
    return f"{m.group(1)}" if m else None

def _to_datetime(ts: str) -> datetime:
    # Tenta normalizar diferentes formatos
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y%m%d%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(ts, fmt)
        except Exception:
            continue
    # fallback: agora
    return datetime.now()

# ----------------------------------------------------------
# Leitura – Auditoria.IA (JSONL)
# ----------------------------------------------------------
def load_auditoria_jsonl() -> List[Dict[str, Any]]:
    """
    Lê todos os arquivos exports/auditoria/audit_*.jsonl e retorna
    uma lista de eventos (dict). Campos típicos:
      - timestamp, artefato, etapa, sha256, word_count, snapshot_relpath, meta
    """
    base = _dir_auditoria()
    if not base.exists():
        return []

    events: List[Dict[str, Any]] = []
    for path in sorted(base.glob("audit_*.jsonl")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        # Anexa info do arquivo (dia)
                        data["_daytag"] = _parse_daytag_from_jsonl(path)
                        events.append(data)
                    except json.JSONDecodeError:
                        # ignora linhas inválidas
                        continue
        except Exception:
            continue
    # Ordena por timestamp (quando possível)
    events.sort(key=lambda d: _to_datetime(d.get("timestamp", d.get("_daytag", ""))))
    return events

# ----------------------------------------------------------
# Leitura – Comparador.IA (relatórios JSON)
# ----------------------------------------------------------
def load_relatorios_coerencia() -> List[Dict[str, Any]]:
    """
    Lê todos os arquivos exports/analises/relatorio_coerencia_*.json e
    retorna lista com dicts contendo a coerência global e comparações.
    Adiciona _stamp (YYYYMMDD) extraído do nome.
    """
    base = _dir_analises()
    if not base.exists():
        return []

    rels: List[Dict[str, Any]] = []
    for path in sorted(base.glob("relatorio_coerencia_*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["_path"] = str(path)
                data["_stamp"] = _parse_stamp_from_relatorio(path) or ""
                rels.append(data)
        except Exception:
            continue

    # Ordena por stamp (YYYYMMDD)
    rels.sort(key=lambda d: d.get("_stamp", ""))
    return rels

# ----------------------------------------------------------
# Agregações / KPIs
# ----------------------------------------------------------
def aggregate_auditoria(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agrega dados de auditoria:
      - total de eventos
      - eventos por artefato
      - último hash/snapshot por artefato
      - word_count médio por artefato
    """
    artefatos = ["DFD", "ETP", "TR", "Edital"]
    out: Dict[str, Any] = {
        "total_eventos": len(events),
        "por_artefato": {a: 0 for a in artefatos},
        "ultimo_hash": {a: "" for a in artefatos},
        "ultimo_snapshot": {a: "" for a in artefatos},
        "word_count_medio": {a: 0 for a in artefatos},
    }

    # Acúmulos
    wc_sum = {a: 0 for a in artefatos}
    wc_cnt = {a: 0 for a in artefatos}

    for e in events:
        art = e.get("artefato")
        if art in out["por_artefato"]:
            out["por_artefato"][art] += 1
            # Atualiza "último" (como está ordenado por timestamp, o loop já garante)
            short_hash = (e.get("sha256") or "")[:10]
            if short_hash:
                out["ultimo_hash"][art] = short_hash
            snap = e.get("snapshot_relpath") or ""
            if snap:
                out["ultimo_snapshot"][art] = snap
            wc = e.get("word_count")
            if isinstance(wc, int):
                wc_sum[art] += wc
                wc_cnt[art] += 1

    # Médias
    for a in artefatos:
        out["word_count_medio"][a] = round(wc_sum[a] / wc_cnt[a], 2) if wc_cnt[a] > 0 else 0

    return out

def aggregate_coerencia(rels: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Constrói séries históricas de coerência global e últimas comparações.
    """
    serie = []
    ult_comp = {}

    for r in rels:
        stamp = r.get("_stamp", "")  # YYYYMMDD
        cg = r.get("coerencia_global", 0)
        serie.append({
            "stamp": stamp,
            "coerencia_global": cg
        })
        # Mantém a última "comparacoes" observada
        if isinstance(r.get("comparacoes"), dict):
            ult_comp = r["comparacoes"]

    return {
        "serie_coerencia": serie,
        "ultima_comparacao": ult_comp
    }

# ----------------------------------------------------------
# Consolidador principal
# ----------------------------------------------------------
def build_governance_snapshot() -> Dict[str, Any]:
    """
    Retorna um "snapshot" com todas as informações necessárias para o painel:
      - auditoria (totais, últimos hashes, médias)
      - coerência (série histórica e última comparação)
    """
    events = load_auditoria_jsonl()
    rels = load_relatorios_coerencia()

    aud = aggregate_auditoria(events)
    coe = aggregate_coerencia(rels)

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "auditoria": aud,
        "coerencia": coe,
        "fontes": {
            "auditoria_files": sorted([p.name for p in _dir_auditoria().glob("audit_*.jsonl")]) if _dir_auditoria().exists() else [],
            "analise_files": sorted([p.name for p in _dir_analises().glob("relatorio_coerencia_*.json")]) if _dir_analises().exists() else [],
        }
    }
