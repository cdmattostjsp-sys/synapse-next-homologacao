"""
analytics_engine_vNext.py – SynapseNext vNext
Módulo de análise e métricas institucionais – SAAB/TJSP
Homologado em: 2025-10-30
"""

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

EXPORTS_DIR = Path("exports")
LOGS_DIR = EXPORTS_DIR / "logs"
METRICS_DIR = EXPORTS_DIR / "analises"
METRICS_DIR.mkdir(parents=True, exist_ok=True)

def carregar_json_seguro(path: Path):
    """Tenta carregar JSON e retorna dicionário vazio em caso de falha."""
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def calcular_tempo_medio_tramitacao(dados_logs):
    """Calcula o tempo médio entre fases da jornada de contratação."""
    resultados = []
    for log in dados_logs:
        fases = log.get("fases", {})
        if all(k in fases for k in ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]):
            dfd = datetime.fromisoformat(fases["DFD"])
            contrato = datetime.fromisoformat(fases["CONTRATO"])
            dias = (contrato - dfd).days
            resultados.append(dias)
    return sum(resultados) / len(resultados) if resultados else 0

def gerar_dataframe_conformidade(artefatos):
    """Gera dataframe com status de conformidade de cada artefato."""
    registros = []
    for nome, dados in artefatos.items():
        registros.append({
            "Artefato": nome,
            "Status": dados.get("status", "Desconhecido"),
            "Alertas": len(dados.get("alertas", [])),
            "Última atualização": dados.get("timestamp", "")
        })
    return pd.DataFrame(registros)

def gerar_insights_dataframe():
    """Gera dataframe consolidado com indicadores de desempenho."""
    print("===================================================")
    print("📊 Gerando métricas e insights – SynapseNext vNext")
    print("===================================================\n")

    validator_files = sorted(EXPORTS_DIR.glob("validator_engine_vNext_*.json"))
    latest_validator = validator_files[-1] if validator_files else None
    validator_data = carregar_json_seguro(latest_validator) if latest_validator else []

    # Métricas baseadas nos artefatos
    conformes = sum(1 for r in validator_data if r.get("status") == "OK")
    incompletos = sum(1 for r in validator_data if r.get("status") == "Incompleto")
    ausentes = sum(1 for r in validator_data if r.get("status") == "Ausente")
    total = len(validator_data) or 1
    conformidade_percentual = round((conformes / total) * 100, 2)

    # Criação de dataframe consolidado
    df = pd.DataFrame({
        "Indicador": [
            "Conformidade Legal (%)",
            "Artefatos Completos",
            "Artefatos Incompletos",
            "Artefatos Ausentes",
            "Total de Artefatos"
        ],
        "Valor": [
            conformidade_percentual,
            conformes,
            incompletos,
            ausentes,
            total
        ]
    })

    # Salvar dataframe como CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = METRICS_DIR / f"insights_metrics_{timestamp}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"✅ Métricas salvas em: {csv_path}")
    return df


def gerar_relatorio_json():
    """Consolida todos os indicadores em um arquivo JSON único."""
    print("📦 Consolidando relatório analítico em formato JSON...")
    df = gerar_insights_dataframe()

    metrics = {
        "data_execucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "indicadores": df.to_dict(orient="records")
    }

    json_path = METRICS_DIR / f"insights_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print(f"✅ Relatório analítico salvo em: {json_path}")
    return json_path


if __name__ == "__main__":
    print("===================================================")
    print("📈 Teste de Geração – analytics_engine_vNext.py")
    print("===================================================\n")
    gerar_relatorio_json()
