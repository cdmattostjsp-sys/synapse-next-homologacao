"""
validator_engine_vNext.py – SynapseNext vNext
Validador de artefatos institucionais – SAAB/TJSP
Homologado em: 2025-10-29
"""

import os
import json
from datetime import datetime
from pathlib import Path

EXPORTS_DIR = Path("exports")
LOGS_DIR = EXPORTS_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

ARQUIVOS_ESPERADOS = {
    "DFD": "dfd_data.json",
    "ETP": "etp_data.json",
    "TR": "tr_data.json",
    "EDITAL": "edital_data.json",
    "CONTRATO": "contrato_data.json",
}

CAMPOS_OBRIGATORIOS = {
    "DFD": ["titulo", "objetivo", "justificativa", "unidade_requisitante"],
    "ETP": ["metodologia", "analise_riscos", "motivacao_tecnica", "responsavel_tecnico"],
    "TR": ["objeto", "especificacao", "criterios_julgamento", "prazo_execucao"],
    "EDITAL": ["objeto", "condicoes_participacao", "criterios_classificacao", "vigencia"],
    "CONTRATO": ["contratante", "contratado", "objeto", "valor", "prazo"],
}


def validar_artefato(tipo: str, caminho: Path):
    """
    Valida o conteúdo de um artefato JSON com base nos campos obrigatórios.
    Retorna dicionário com resultado e alertas.
    """
    resultado = {"tipo": tipo, "arquivo": str(caminho), "status": "OK", "alertas": []}

    if not caminho.exists():
        resultado["status"] = "Ausente"
        resultado["alertas"].append(f"⚠️ Arquivo {caminho.name} não encontrado.")
        return resultado

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        resultado["status"] = "Erro"
        resultado["alertas"].append(f"❌ Erro ao ler {caminho.name}: {e}")
        return resultado

    campos = CAMPOS_OBRIGATORIOS.get(tipo, [])
    for campo in campos:
        if campo not in data or not data[campo]:
            resultado["status"] = "Incompleto"
            resultado["alertas"].append(f"🟠 Campo obrigatório ausente: {campo}")

    if resultado["status"] == "OK":
        resultado["alertas"].append("🟢 Estrutura válida e completa.")

    return resultado


def gerar_relatorio(resultados: list):
    """
    Gera relatório TXT e JSON com os resultados da validação.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = EXPORTS_DIR / f"validator_engine_vNext_{timestamp}.txt"
    json_path = EXPORTS_DIR / f"validator_engine_vNext_{timestamp}.json"

    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write("==============================================\n")
        txt_file.write("🧩 Validador de Artefatos – SynapseNext vNext\n")
        txt_file.write("==============================================\n\n")

        for r in resultados:
            txt_file.write(f"{r['tipo']} → {r['status']}\n")
            for alerta in r["alertas"]:
                txt_file.write(f"   - {alerta}\n")
            txt_file.write("\n")

        txt_file.write("==============================================\n")
        txt_file.write(f"📄 Relatório salvo em: {txt_path}\n")
        txt_file.write("==============================================\n")

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(resultados, jf, ensure_ascii=False, indent=2)

    print(f"✅ Relatórios gerados: {txt_path.name} e {json_path.name}")
    return txt_path, json_path


def validar_todos():
    """
    Executa a validação de todos os artefatos esperados.
    """
    print("===================================================")
    print("🧩 Validador de Artefatos – SynapseNext vNext")
    print("===================================================\n")

    resultados = []
    for tipo, nome_arquivo in ARQUIVOS_ESPERADOS.items():
        caminho = EXPORTS_DIR / nome_arquivo
        resultado = validar_artefato(tipo, caminho)
        status = resultado["status"]
        cor = "🟢" if status == "OK" else "🟠" if status == "Incompleto" else "🔴"
        print(f"{cor} {tipo}: {status}")
        resultados.append(resultado)

    txt_path, json_path = gerar_relatorio(resultados)
    print(f"\n📁 Logs salvos em: {LOGS_DIR}")
    print("===================================================\n")
    return resultados


if __name__ == "__main__":
    validar_todos()
