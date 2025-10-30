# -*- coding: utf-8 -*-
"""
utils/alertas_pipeline.py
-------------------------
Pipeline institucional de alertas – SynapseNext vNext
Responsável por analisar snapshots de governança, métricas de desempenho
e artefatos exportados, gerando alertas automáticos classificados por severidade.

Instituição: SAAB / TJSP
Autor: Synapse.Engineer
Data: 2025-10-30
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ======================================================
# 🔧 Parâmetros institucionais padrão
# ======================================================
DEFAULTS = {
    "threshold_coerencia": 0.85,
    "limite_alertas": 10,
    "severidades": ["baixo", "medio", "alto"],
    "origem": "SAAB/TJSP",
}

# ======================================================
# 🧠 Função principal: gerar alertas automáticos
# ======================================================
def gerar_alertas(snapshot: dict = None) -> list:
    """
    Gera uma lista de alertas com base no snapshot de governança
    e nas métricas institucionais disponíveis.
    """
    alertas = []

    if not snapshot:
        alertas.append({
            "severidade": "alto",
            "area": "Governança",
            "artefato": "snapshot",
            "mensagem": "Nenhum snapshot de governança foi fornecido.",
            "recomendacao": "Execute novamente a geração de governança antes da análise."
        })
        return alertas

    coerencia = snapshot.get("coerencia_global", 0)
    artefatos = snapshot.get("artefatos", 0)

    if coerencia < DEFAULTS["threshold_coerencia"] * 100:
        alertas.append({
            "severidade": "medio",
            "area": "Governança",
            "artefato": "coerencia_global",
            "mensagem": f"Coerência abaixo do limiar: {coerencia:.1f}%.",
            "recomendacao": "Revisar ETP e TR para garantir consistência documental."
        })

    if artefatos < 3:
        alertas.append({
            "severidade": "alto",
            "area": "Insumos",
            "artefato": "artefatos",
            "mensagem": f"Apenas {artefatos} artefatos processados.",
            "recomendacao": "Verifique se todos os módulos foram executados corretamente."
        })

    if not alertas:
        alertas.append({
            "severidade": "baixo",
            "area": "Auditoria",
            "artefato": "rotina",
            "mensagem": "Nenhuma inconsistência detectada.",
            "recomendacao": "Sistema operando dentro dos parâmetros esperados."
        })

    return alertas[:DEFAULTS["limite_alertas"]]

# ======================================================
# 📊 Função de avaliação genérica de alertas
# ======================================================
def evaluate_alerts(snapshot: dict) -> dict:
    """Retorna contagem agregada de alertas por severidade."""
    alertas = gerar_alertas(snapshot)
    total = len(alertas)
    severidades = {nivel: 0 for nivel in DEFAULTS["severidades"]}
    for a in alertas:
        severidades[a["severidade"]] += 1
    return {"total": total, "por_nivel": severidades, "detalhes": alertas}

# ======================================================
# 💾 Exportação institucional de alertas
# ======================================================
def export_alerts_json(data: dict) -> str:
    """Exporta alertas em formato JSON institucional."""
    export_dir = Path("exports/analises")
    export_dir.mkdir(parents=True, exist_ok=True)

    filename = f"alertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = export_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return str(filepath)

# ======================================================
# 🧪 Execução isolada de teste
# ======================================================
if __name__ == "__main__":
    exemplo_snapshot = {"coerencia_global": 82.4, "artefatos": 2}
    alertas = gerar_alertas(exemplo_snapshot)
    print("✅ Alertas gerados:")
    for a in alertas:
        print(f" - [{a['severidade'].upper()}] {a['mensagem']}")
    path = export_alerts_json({"gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "alertas": alertas})
    print(f"\n💾 Arquivo salvo em: {path}")
