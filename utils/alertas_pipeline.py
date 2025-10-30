# -*- coding: utf-8 -*-
"""
alertas_pipeline.py – Módulo institucional SAAB/TJSP
==============================================================
Responsável por consolidar análises de coerência documental
e gerar alertas automáticos de auditoria técnica.

Versão: SynapseNext vNext
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
    "peso_risco": 0.25
}

# ======================================================
# 📊 Função: avaliar alertas
# ======================================================
def evaluate_alerts(df_coerencia=None, coerencia_global=80, pairwise_min=70):
    """
    Gera uma lista simulada de alertas de coerência.
    """
    resultados = [
        {
            "id": 1,
            "categoria": "Coerência Global",
            "descricao": "A coerência geral do documento está abaixo do limiar esperado.",
            "valor": coerencia_global,
            "limiar": DEFAULTS["min_coerencia_global"],
            "status": "Crítico" if coerencia_global < DEFAULTS["min_coerencia_global"] else "OK",
        },
        {
            "id": 2,
            "categoria": "Coerência Par-a-Par",
            "descricao": "Foram identificadas seções com baixa correlação semântica.",
            "valor": pairwise_min,
            "limiar": DEFAULTS["min_pairwise"],
            "status": "Atenção" if pairwise_min < DEFAULTS["min_pairwise"] else "OK",
        }
    ]
    return resultados

# ======================================================
# 💾 Função: exportar alertas para JSON
# ======================================================
def export_alerts_json(alertas, export_path="exports/analises"):
    os.makedirs(export_path, exist_ok=True)
    file_path = os.path.join(export_path, f"alertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)
    return file_path
