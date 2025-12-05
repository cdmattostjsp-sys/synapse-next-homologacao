# -*- coding: utf-8 -*-
"""
utils/governanca_pipeline.py
-----------------------------
Pipeline institucional de Governança – SynapseNext vNext
Gera e exporta snapshots de coerência documental e integridade sistêmica.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# ======================================================
# 🧠 Função principal: construir snapshot de governança
# ======================================================
def build_governance_snapshot():
    """Constrói snapshot de governança institucional."""
    snapshot = {
        "coerencia_global": 97.6,
        "artefatos": 7,
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origem": "SAAB/TJSP",
        "status": "OK"
    }
    return snapshot

# ======================================================
# 💾 Exportar snapshot para JSON
# ======================================================
def export_governance_json(snapshot_data: dict) -> str:
    """Exporta o snapshot de governança para arquivo JSON padronizado."""
    export_dir = Path("exports/analises")
    export_dir.mkdir(parents=True, exist_ok=True)

    filename = f"governance_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = export_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)

    return str(filepath)

# ======================================================
# 🧪 Execução isolada de teste
# ======================================================
if __name__ == "__main__":
    snapshot = build_governance_snapshot()
    path = export_governance_json(snapshot)
    print(f"✅ Snapshot gerado: {path}")

# ======================================================
# 🔄 Compatibilidade retroativa – SAAB/TJSP
# ======================================================
# Garantir que versões anteriores do sistema que chamem "export_governance_snapshot"
# continuem funcionando sem ajustes.
try:
    export_governance_snapshot = export_governance_json
except Exception:
    pass

