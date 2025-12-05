"""
diagnostic_fase3_vNext.py – SynapseNext vNext
Diagnóstico técnico e auditoria institucional – SAAB/TJSP
Homologado em: 2025-10-29
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Diretórios esperados
BASE_DIR = Path(".")
EXPORTS_DIR = BASE_DIR / "exports"
AGENTS_DIR = BASE_DIR / "agents"
UTILS_DIR = BASE_DIR / "utils"
PAGES_DIR = BASE_DIR / "streamlit_app" / "pages"
KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"
PROMPTS_DIR = BASE_DIR / "prompts"

# Saída
EXPORTS_DIR.mkdir(exist_ok=True)
LOGS_DIR = EXPORTS_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

def verificar_diretorios():
    esperados = [
        AGENTS_DIR, UTILS_DIR, PAGES_DIR,
        KNOWLEDGE_DIR, PROMPTS_DIR, EXPORTS_DIR
    ]
    resultados = {}
    for pasta in esperados:
        resultados[str(pasta)] = pasta.exists()
    return resultados

def listar_arquivos(pasta: Path, extensao: str = ".py"):
    if not pasta.exists():
        return []
    return [f.name for f in pasta.glob(f"*{extensao}")]

def testar_escrita_export():
    teste_path = EXPORTS_DIR / "test_write.txt"
    try:
        with open(teste_path, "w", encoding="utf-8") as f:
            f.write("Teste de escrita SynapseNext vNext\n")
        return True
    except Exception:
        return False

def gerar_relatorio(resultados):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio_path = EXPORTS_DIR / f"diagnostic_fase3_vNext_{timestamp}.txt"

    with open(relatorio_path, "w", encoding="utf-8") as f:
        f.write("============================================================\n")
        f.write("🔍 Diagnóstico Técnico – SynapseNext vNext (Fase 3)\n")
        f.write("============================================================\n\n")

        f.write("🧱 Estrutura de diretórios:\n")
        for k, v in resultados["diretorios"].items():
            f.write(f" - {k}: {'OK' if v else '❌ Ausente'}\n")

        f.write("\n🤖 Agentes detectados:\n")
        for ag in resultados["agentes"]:
            f.write(f" - {ag}\n")

        f.write("\n🧰 Módulos utilitários:\n")
        for u in resultados["utils"]:
            f.write(f" - {u}\n")

        f.write("\n📄 Páginas Streamlit:\n")
        for p in resultados["pages"]:
            f.write(f" - {p}\n")

        f.write("\n�� Base de conhecimento:\n")
        for kb in resultados["knowledge"]:
            f.write(f" - {kb}\n")

        f.write("\n📂 Teste de escrita em /exports/: ")
        f.write("OK\n" if resultados["escrita_ok"] else "❌ Falhou\n")

        f.write("\n============================================================\n")
        f.write(f"📄 Relatório salvo em: {relatorio_path}\n")
        f.write("============================================================\n")

    print(f"✅ Relatório de diagnóstico técnico gerado: {relatorio_path}")
    return relatorio_path


def executar_diagnostico():
    print("============================================================")
    print("🔍 Executando Diagnóstico Técnico – SynapseNext vNext")
    print("============================================================\n")

    resultados = {
        "diretorios": verificar_diretorios(),
        "agentes": listar_arquivos(AGENTS_DIR),
        "utils": listar_arquivos(UTILS_DIR),
        "pages": listar_arquivos(PAGES_DIR),
        "knowledge": listar_arquivos(KNOWLEDGE_DIR, ".txt") + listar_arquivos(KNOWLEDGE_DIR, ".docx"),
        "escrita_ok": testar_escrita_export(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    gerar_relatorio(resultados)
    print("\n🧠 Diagnóstico concluído com sucesso!\n")
    return resultados


if __name__ == "__main__":
    executar_diagnostico()
