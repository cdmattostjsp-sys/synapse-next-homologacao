# utils/insights_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 11D – Insights Históricos)
# Consolida séries temporais a partir de:
#  - Auditoria.IA  → exports/auditoria/audit_*.jsonl
#  - Comparador.IA → exports/analises/relatorio_coerencia_*.json
# Entregas:
#  - build_insights(): snapshot com métricas e séries temporais
#  - export_insights_json(): salva insights_YYYYMMDD_HHMM.json
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
from collections import defaultdict
import math

ARTEFATOS = ["DFD", "ETP", "TR", "Edital"]

# ----------------------------------------------------------
# Caminhos
# ----------------------------------------------------------
def _root() -> Path:
    return Path(__file__).resolve().parents[1]

def _dir_auditoria() -> Path:
    return _root() / "exports" / "auditoria"

def _dir_analises() -> Path:
    return _root() / "exports" / "analises"

def _ensure_out() -> Path:
    out = _dir_analises()
    out.mkdir(parents=True, exist_ok=True)
    return out

# ----------------------------------------------------------
# Imports de pipelines existentes (com fallback elegante)
# ----------------------------------------------------------
try:
    from utils.governanca_pipeline import load_auditoria_jsonl, load_relatorios_coerencia
except Exception as e:
    # Fallback mínimo (se governanca_pipeline não estiver disponível)
    def load_auditoria_jsonl() -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        base = _dir_auditoria()
        if not base.exists():
            return events
        for p in sorted(base.glob("audit_*.jsonl")):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        events.append(data)
                    except Exception:
                        continue
        return events

    def load_relatorios_coerencia() -> List[Dict[str, Any]]:
        rels: List[Dict[str, Any]] = []
        base = _dir_analises()
        if not base.exists():
            return rels
        for p in sorted(base.glob("relatorio_coerencia_*.json")):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["_path"] = str(p)
                    rels.append(data)
            except Exception:
                continue
        return rels

# ----------------------------------------------------------
# Datetime helpers
# ----------------------------------------------------------
def _to_dt(ts: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%Y%m%d%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(ts, fmt)
        except Exception:
            continue
    return datetime.now()

def _to_daykey(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")

# ----------------------------------------------------------
# Núcleo de Insights
# ----------------------------------------------------------
def _rolling_mean(values: List[float], window: int) -> List[float]:
    if window <= 1:
        return values[:]
    out: List[float] = []
    run = 0.0
    q: List[float] = []
    for v in values:
        q.append(v)
        run += v
        if len(q) > window:
            run -= q.pop(0)
        out.append(round(run / len(q), 2))
    return out

def build_insights() -> Dict[str, Any]:
    """
    Retorna um snapshot com:
      - eventos por dia (total e por artefato)
      - word_count médio por dia/artefato
      - variação percentual recente de word_count (últimos 2 eventos)
      - série de coerência global + média móvel (janela 3)
    """
    events = load_auditoria_jsonl()
    rels = load_relatorios_coerencia()

    # --- Auditoria por dia ---
    by_day_total = defaultdict(int)
    by_day_art = {a: defaultdict(int) for a in ARTEFATOS}

    # --- Word count médio por dia/artefato ---
    wc_acc = {a: defaultdict(lambda: {"sum": 0, "n": 0}) for a in ARTEFATOS}

    # --- Variação de word count (últimos 2 eventos) ---
    last_wc = {a: [] for a in ARTEFATOS}

    for e in events:
        ts = e.get("timestamp") or e.get("_daytag") or ""
        dt = _to_dt(ts)
        day = _to_daykey(dt)
        art = e.get("artefato", "")
        if art in ARTEFATOS:
            by_day_total[day] += 1
            by_day_art[art][day] += 1

            wc = e.get("word_count")
            if isinstance(wc, int):
                wc_acc[art][day]["sum"] += wc
                wc_acc[art][day]["n"] += 1
                # para variação recente
                last_wc[art].append((dt, wc))

    # médias de wc por dia/artefato
    wc_day_avg = {a: [] for a in ARTEFATOS}
    for a in ARTEFATOS:
        for day in sorted(wc_acc[a].keys()):
            d = wc_acc[a][day]
            avg = round(d["sum"] / max(1, d["n"]), 2)
            wc_day_avg[a].append({"day": day, "avg_wc": avg})

    # variação de wc (últimos 2)
    wc_delta_recent = {}
    for a in ARTEFATOS:
        if len(last_wc[a]) >= 2:
            last_wc[a].sort(key=lambda t: t[0])
            prev = last_wc[a][-2][1]
            lastv = last_wc[a][-1][1]
            if prev > 0:
                pct = round((lastv - prev) * 100.0 / prev, 2)
            else:
                pct = 0.0
            wc_delta_recent[a] = {"prev": prev, "last": lastv, "delta_pct": pct}
        elif len(last_wc[a]) == 1:
            wc_delta_recent[a] = {"prev": None, "last": last_wc[a][-1][1], "delta_pct": None}
        else:
            wc_delta_recent[a] = {"prev": None, "last": None, "delta_pct": None}

    # séries de coerência global
    coherence_series = []
    for r in rels:
        # tentativas de obter data: do nome ou do conteúdo
        stamp = r.get("_stamp") or r.get("timestamp") or ""
        dt = _to_dt(stamp) if stamp else datetime.now()
        ymd = _to_daykey(dt)
        cg = r.get("coerencia_global", 0)
        coherence_series.append({"day": ymd, "coerencia_global": cg})
    coherence_series.sort(key=lambda x: x["day"])

    # média móvel (janela 3)
    coh_vals = [c["coerencia_global"] for c in coherence_series]
    coh_ma = _rolling_mean(coh_vals, window=3)
    coherence_ma_series = [
        {"day": coherence_series[i]["day"], "ma": coh_ma[i]} for i in range(len(coherence_series))
    ]

    # volume por dia (total)
    volume_series = [{"day": d, "events": by_day_total[d]} for d in sorted(by_day_total.keys())]

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "volume_por_dia": volume_series,
        "volume_por_artefato": {
            a: [{"day": d, "events": by_day_art[a][d]} for d in sorted(by_day_art[a].keys())]
            for a in ARTEFATOS
        },
        "wc_day_avg": wc_day_avg,
        "wc_delta_recent": wc_delta_recent,
        "coherence_series": coherence_series,
        "coherence_ma_series": coherence_ma_series,
        "fontes": {
            "auditoria_files": sorted([p.name for p in _dir_auditoria().glob("audit_*.jsonl")]) if _dir_auditoria().exists() else [],
            "analise_files": sorted([p.name for p in _dir_analises().glob("relatorio_coerencia_*.json")]) if _dir_analises().exists() else [],
        }
    }

# ----------------------------------------------------------
# Export
# ----------------------------------------------------------
def export_insights_json(payload: Dict[str, Any]) -> str:
    """
    Salva build_insights() em JSON para consumo externo (BI).
    """
    out = _ensure_out()
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = out / f"insights_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return str(path)
