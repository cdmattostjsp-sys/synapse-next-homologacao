# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – 2025-11-05
# ==========================================================

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

from utils.integration_ai_engine import gerar_campos_por_ia


# ==========================================================
# 📁 Definições de diretórios
# ==========================================================
def get_json_export_dir():
    """
    Retorna o diretório de exportação gravável.
    Se o diretório padrão não for gravável, usa /tmp.
    """
    base_path = Path("exports") / "insumos" / "json"
    try:
        base_path.mkdir(parents=True, exist_ok=True)
        # Teste de escrita
        test_file = base_path / "_test_write.txt"
        with open(test_file, "w") as f:
            f.write("ok")
        test_file.unlink()
        return base_path
    except Exception:
        tmp_path = Path(tempfile.gettempdir()) / "insumos" / "json"
        tmp_path.mkdir(parents=True, exist_ok=True)
        return tmp_path


# ==========================================================
# 💾 Funções principais
# ==========================================================
def salvar_insumo(uploaded_file, artefato: str):
    """
    Salva o arquivo enviado dentro de exports/insumos/json/
    ou em /tmp, garantindo diretório disponível.
    """
    base_dir = get_json_export_dir()
    filename = f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_path = base_dir / filename

    meta = {
        "nome": uploaded_file.name,
        "artefato": artefato,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return save_path


def processar_insumo(uploaded_file, artefato: str):
    """
    Processa o insumo com IA e salva o resultado como JSON.
    """
    try:
        # Etapa 1: análise por IA (prompt interno)
        campos_ai = gerar_campos_por_ia(uploaded_file, artefato)

        # Etapa 2: salvamento robusto
        base_dir = get_json_export_dir()
        json_path = base_dir / f"{artefato}_ultimo.json"

        resultado = {
            "artefato": artefato,
            "arquivo_origem": uploaded_file.name,
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campos_ai": campos_ai or {},
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"[SynapseNext] JSON salvo em: {json_path}")
        return resultado

    except Exception as e:
        print(f"[ERRO] Falha ao processar insumo: {e}")
        return {"erro": str(e)}


def listar_insumos():
    """
    Lista arquivos JSON disponíveis no diretório de exportação.
    """
    base_dir = get_json_export_dir()
    arquivos = list(base_dir.glob("*.json"))
    return [f.name for f in arquivos]
