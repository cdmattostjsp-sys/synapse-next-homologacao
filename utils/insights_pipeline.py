# -*- coding: utf-8 -*-
"""
utils/insights_pipeline.py
---------------------------
Pipeline de Análise de Desempenho Institucional – SynapseNext vNext
Gera métricas, tendências e análises de coerência entre os módulos do sistema.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ======================================================
# 🧠 Construção das métricas institucionais
# ======================================================
def build_insights():
    """Gera dados de desempenho simulados/institucionais."""
    volume_tempo = [
        {"data": "2025-10-01", "valor": 10},
        {"data": "2025-10-05", "valor": 14},
        {"data": "2025-10-10", "valor": 17},
        {"data": "2025-10-15", "valor": 21},
        {"data": "2025-10-20", "valor": 19},
        {"data": "2025-10-25", "valor": 24},
        {"data": "2025-10-30", "valor": 26},
    ]

    insights = {
        "resumo": {
            "total_execucoes": 7,
            "coerencia_media": 96.2,
            "ultima_execucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "volume_tempo": volume_tempo,
        "origem": "SAAB/TJSP",
    }

    return insights

# ======================================================
# 💾 Exportar insights em formato JSON
# ======================================================
def export_insights_json(data: dict) -> str:
    """Exporta o dicionário de insights para um arquivo JSON."""
    export_dir = Path("exports/analises")
    export_dir.mkdir(parents=True, exist_ok=True)

    filename = f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = export_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(filepath)

# ======================================================
# 🧪 Execução isolada de teste
# ======================================================
if __name__ == "__main__":
    insights = build_insights()
    path = export_insights_json(insights)
    print(f"✅ Insights exportados com sucesso: {path}")

# ======================================================
# 🔄 Compatibilidade retroativa – SAAB/TJSP
# ======================================================
# Mantém suporte a imports antigos usados em versões pré-vNext.
try:
    export_insights = export_insights_json
except Exception:
    pass
