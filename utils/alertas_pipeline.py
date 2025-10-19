# utils/alertas_pipeline.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 11C – Alertas Proativos)
# Regras de alerta baseadas em:
#   - Auditoria (eventos, "staleness"/desatualização, variação de tamanho)
#   - Coerência Global e comparações par-a-par (Comparador.IA)
#
# Saída:
#   - Lista de alertas estruturados (id, área, severidade, artefato, título,
#     detalhe, recomendação, timestamp)
#   - Exportação opcional para JSON em exports/analises/
# ==========================================================

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

# ---------------------------------------------------------------------
# Imports do pipeline de governança (já existentes no projeto)
# ---------------------------------------------------------------------
try:
    from utils.governanca_pipeline import (
        build_governance_snapshot,
        load_auditoria_jsonl,
        load_relatorios_coerencia,
    )
except Exception as e:
    # Permite teste isolado do módulo.
    print(f"[alertas_pipeline] Aviso: falha ao importar governanca_pipeline: {e}")
    build_governance_snapshot = None
    load_auditoria_jsonl = lambda: []         # type: ignore
    load_relatorios_coerencia = lambda: []    # type: ignore


# ---------------------------------------------------------------------
# Configurações padrão
# ---------------------------------------------------------------------
DEFAULTS = {
    "min_coerencia_global": 70,   # % mínimo aceitável para coerência global
    "min_pairwise": 65,           # % mínimo para comparações diretas (DFD↔ETP, ETP↔TR, TR↔Edital)
    "max_staleness_days": 7,      # dias máximos sem novos eventos de auditoria
    "max_wc_change_pct": 30,      # % máx. de variação (absoluta) entre os 2 últimos snapshots
}

ARTEFATOS = ["DFD", "ETP", "TR", "Edital"]


# ---------------------------------------------------------------------
# Utilitário local de datas (flexível)
# ---------------------------------------------------------------------
def _to_dt(ts: str) -> datetime:
    for fmt in (
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y%m%d%H%M%S",
        "%Y%m%d",
    ):
        try:
            return datetime.strptime(ts, fmt)
        except Exception:
            continue
    return datetime.now()


def _now() -> datetime:
    return datetime.now()


# ---------------------------------------------------------------------
# Regras de alerta
# ---------------------------------------------------------------------
def _alert(
    _id: str,
    area: str,
    severidade: str,
    titulo: str,
    detalhe: str,
    recomendacao: str,
    artefato: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "id": _id,
        "area": area,
        "severidade": severidade,   # alto | medio | baixo
        "artefato": artefato or "",
        "titulo": titulo,
        "detalhe": detalhe,
        "recomendacao": recomendacao,
        "timestamp": _now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def _group_events_by_artifact(events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    out: Dict[str, List[Dict[str, Any]]] = {a: [] for a in ARTEFATOS}
    for e in events:
        a = e.get("artefato")
        if a in out:
            out[a].append(e)
    # Ordena por timestamp
    for a in out:
        out[a].sort(key=lambda d: _to_dt(d.get("timestamp", d.get("_daytag", ""))))
    return out


def evaluate_alerts(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Varre os dados de auditoria e coerência e retorna
    um dicionário com os alertas encontrados e métricas.
    """
    cfg = {**DEFAULTS, **(config or {})}

    # Fontes
    snapshot = build_governance_snapshot() if build_governance_snapshot else {}
    events = load_auditoria_jsonl()
    rels = load_relatorios_coerencia()

    alerts: List[Dict[str, Any]] = []

    # -----------------------------------------------------------------
    # REGRAS – Auditoria
    # -----------------------------------------------------------------
    by_art = _group_events_by_artifact(events)

    # (A) Sem auditoria registrada
    for a in ARTEFATOS:
        if len(by_art[a]) == 0:
            alerts.append(_alert(
                _id=f"AUD-NOEVT-{a}",
                area="Auditoria",
                severidade="medio",
                titulo=f"{a}: sem eventos de auditoria",
                detalhe=f"Não há registros em 'exports/auditoria' para o artefato {a}.",
                recomendacao="Gerar pelo menos um snapshot institucional (rascunho) para iniciar a trilha de auditoria.",
                artefato=a,
            ))

    # (B) Staleness (tempo sem novos eventos)
    for a, lst in by_art.items():
        if not lst:
            continue
        last_ts = lst[-1].get("timestamp") or lst[-1].get("_daytag", "")
        days = (_now() - _to_dt(last_ts)).days
        if days > cfg["max_staleness_days"]:
            alerts.append(_alert(
                _id=f"AUD-STALE-{a}",
                area="Auditoria",
                severidade="medio",
                titulo=f"{a}: desatualizado ({days} dias sem novos eventos)",
                detalhe=f"O último evento do artefato {a} ocorreu há {days} dias.",
                recomendacao=f"Gerar novo snapshot ou revisar o artefato. Parâmetro atual: {cfg['max_staleness_days']} dias.",
                artefato=a,
            ))

    # (C) Variação abrupta de tamanho (word_count)
    for a, lst in by_art.items():
        if len(lst) < 2:
            continue
        wc_last = lst[-1].get("word_count")
        wc_prev = lst[-2].get("word_count")
        if isinstance(wc_last, int) and isinstance(wc_prev, int) and wc_prev > 0:
            pct = abs(wc_last - wc_prev) * 100.0 / wc_prev
            if pct > cfg["max_wc_change_pct"]:
                alerts.append(_alert(
                    _id=f"AUD-WCVAR-{a}",
                    area="Conteúdo",
                    severidade="baixo",
                    titulo=f"{a}: variação abrupta de tamanho ({pct:.1f}%)",
                    detalhe=f"Entre os dois últimos snapshots, a contagem de palavras mudou {pct:.1f}%.",
                    recomendacao=f"Verifique se houve inclusão/remoção significativa. Parâmetro atual: {cfg['max_wc_change_pct']}%.",
                    artefato=a,
                ))

    # -----------------------------------------------------------------
    # REGRAS – Coerência (Comparador.IA)
    # -----------------------------------------------------------------
    serie = snapshot.get("coerencia", {}).get("serie_coerencia", [])
    ultima_comp = snapshot.get("coerencia", {}).get("ultima_comparacao", {})

    # (D) Coerência Global baixa
    if serie:
        last_cg = serie[-1].get("coerencia_global", 0)
        if last_cg < cfg["min_coerencia_global"]:
            alerts.append(_alert(
                _id="COH-LOW",
                area="Coerência",
                severidade="alto",
                titulo=f"Coerência Global baixa ({last_cg}%)",
                detalhe=f"A coerência média entre artefatos ficou abaixo de {cfg['min_coerencia_global']}%.",
                recomendacao="Revisar DFD, ETP e TR para garantir alinhamento de objetivo, escopo e critérios.",
            ))
    else:
        # Sem dados de coerência
        alerts.append(_alert(
            _id="COH-NODATA",
            area="Coerência",
            severidade="baixo",
            titulo="Sem relatórios de coerência",
            detalhe="Não foram encontrados relatórios em `exports/analises/relatorio_coerencia_*.json`.",
            recomendacao="Gerar um relatório de coerência a partir do Comparador.IA.",
        ))

    # (E) Comparações par-a-par abaixo do mínimo
    pair_threshold = cfg["min_pairwise"]
    pairs_of_interest = [
        ("DFD", "ETP"),
        ("ETP", "TR"),
        ("TR", "Edital"),
    ]

    # os nomes no snapshot são "DFD-ETP", "ETP-TR", "TR-Edital"
    for a, b in pairs_of_interest:
        key = f"{a}-{b}"
        val = ultima_comp.get(key)
        if isinstance(val, (int, float)) and val < pair_threshold:
            alerts.append(_alert(
                _id=f"PAIR-LOW-{a}-{b}",
                area="Coerência",
                severidade="alto",
                titulo=f"Similaridade baixa: {a} ↔ {b} ({val}%)",
                detalhe=f"A comparação entre {a} e {b} ficou abaixo de {pair_threshold}%.",
                recomendacao=f"Revisar argumento do {a} e requisitos do {b} para reduzir divergências.",
            ))

    # -----------------------------------------------------------------
    # Consolida métricas
    # -----------------------------------------------------------------
    counts = {"alto": 0, "medio": 0, "baixo": 0}
    for a in alerts:
        sev = a.get("severidade", "baixo")
        if sev in counts:
            counts[sev] += 1

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "parametros": cfg,
        "totais": {"geral": len(alerts), **counts},
        "alerts": alerts,
    }


# ---------------------------------------------------------------------
# Exportação
# ---------------------------------------------------------------------
def _export_dir() -> Path:
    out = Path(__file__).resolve().parents[1] / "exports" / "analises"
    out.mkdir(parents=True, exist_ok=True)
    return out


def export_alerts_json(payload: Dict[str, Any]) -> str:
    """
    Salva o resultado de evaluate_alerts() em JSON.
    Retorna o caminho absoluto do arquivo.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = _export_dir() / f"alertas_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return str(path)
