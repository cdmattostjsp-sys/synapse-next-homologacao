# utils/export_snapshot.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 11B – Exportação do Snapshot Institucional)
# Gera arquivo JSON consolidado com dados de governança
# para uso em Power BI, CNJ, ou auditorias internas.
# ==========================================================

from pathlib import Path
from datetime import datetime
import json

try:
    from utils.governanca_pipeline import build_governance_snapshot
except Exception as e:
    print(f"Erro ao importar governanca_pipeline: {e}")
    build_governance_snapshot = None


def _export_dir() -> Path:
    """Define o diretório padrão para exportação dos snapshots"""
    path = Path(__file__).resolve().parents[1] / "exports" / "analises"
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_snapshot_json() -> str:
    """
    Gera snapshot consolidado e exporta como JSON.
    Retorna o caminho absoluto do arquivo salvo.
    """
    if not build_governance_snapshot:
        raise RuntimeError("Pipeline de governança não encontrado.")

    snapshot = build_governance_snapshot()
    snapshot["versao"] = "11B"
    snapshot["descricao"] = "Snapshot institucional consolidado (Painel de Governança)"

    # Nome com timestamp
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"governanca_snapshot_{ts}.json"
    path = _export_dir() / filename

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise RuntimeError(f"Erro ao salvar snapshot: {e}")

    return str(path)
