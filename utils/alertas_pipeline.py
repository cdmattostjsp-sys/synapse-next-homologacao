# -*- coding: utf-8 -*-
"""
alertas_pipeline.py – Módulo institucional SAAB/TJSP
==============================================================
Responsável por consolidar análises de coerência documental
e gerar alertas automáticos de auditoria técnica.

Versão: SynapseNext vNext (compatível com Alertas + Governança)
==============================================================
"""

import json
import os
from datetime import datetime

# ======================================================
# 🔧 Configurações padrão (DEFAULTS)
# ======================================================
DEFAULTS = {
    "min_coerencia_global": 75,
    "min_pairwise": 70,
    "min_similaridade_tematica": 60,
    "alerta_critico": 50,
    "peso_risco": 0.25,
    "max_staleness_days": 15,  # 🆕 usado na página 09_⚠️ Alertas.py
    "max_wc_change_pct": 25,   # 🆕 compatível com sliders existentes
}

# ======================================================
# 📊 Função: avaliar alertas (usada por 09_⚠️ Alertas.py)
# ======================================================
def evaluate_alerts(df_coerencia=None, coerencia_global=80, pairwise_min=70):
    """
    Gera uma lista simulada de alertas de coerência.
    Retorno compatível com 09_⚠️ Alertas.py (vNext).
    """
    resultados = [
        {
            "id": 1,
            "categoria": "Coerência Global",
            "descricao": "A coerência geral do documento está abaixo do limiar esperado.",
            "valor": coerencia_global,
            "limiar": DEFAULTS["min_coerencia_global"],
            "status": "Crítico" if coerencia_global < DEFAULTS["min_coerencia_global"] else "OK",
            "severidade": "alto" if coerencia_global < 60 else "medio",
            "area": "Análise de Conteúdo",
            "artefato": "ETP.json",
            "mensagem": "Baixa coerência global detectada.",
            "recomendacao": "Revisar estrutura textual do ETP e reexecutar a validação.",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        },
        {
            "id": 2,
            "categoria": "Coerência Par-a-Par",
            "descricao": "Foram identificadas seções com baixa correlação semântica.",
            "valor": pairwise_min,
            "limiar": DEFAULTS["min_pairwise"],
            "status": "Atenção" if pairwise_min < DEFAULTS["min_pairwise"] else "OK",
            "severidade": "medio" if pairwise_min < 70 else "baixo",
            "area": "Estrutura Documental",
            "artefato": "DFD.json",
            "mensagem": "Baixa coerência entre seções correlatas.",
            "recomendacao": "Revisar interdependências de seções e critérios de coerência.",
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        },
    ]

    totais = {
        "geral": len(resultados),
        "alto": sum(1 for r in resultados if r["severidade"] == "alto"),
        "medio": sum(1 for r in resultados if r["severidade"] == "medio"),
        "baixo": sum(1 for r in resultados if r["severidade"] == "baixo"),
    }

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "totais": totais,
        "alerts": resultados,
        "params": DEFAULTS,
    }

# ======================================================
# 💾 Função: exportar alertas para JSON
# ======================================================
def export_alerts_json(alertas, export_path="exports/analises"):
    os.makedirs(export_path, exist_ok=True)
    file_path = os.path.join(
        export_path, f"alertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)
    return file_path

# ======================================================
# 🧩 Wrapper compatível: gerar_alertas(snapshot)
# ======================================================
def gerar_alertas(snapshot=None):
    """
    Compatibilidade para o Painel de Governança.
    Usa evaluate_alerts internamente, com dados resumidos do snapshot.
    """
    coerencia_global = 80
    pairwise_min = 70
    if snapshot and isinstance(snapshot, dict):
        coerencia_global = snapshot.get("coerencia_global", coerencia_global)
        pairwise_min = snapshot.get("pairwise_min", pairwise_min)

    result = evaluate_alerts(
        coerencia_global=coerencia_global,
        pairwise_min=pairwise_min
    )
    return result.get("alerts", [])

