# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – 2025-11-06
# ==========================================================

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

# ==========================================================
# 📦 Integração com o motor institucional de IA
# ==========================================================
from utils.integration_ai_engine import processar_insumo as processar_insumo_ia


# ==========================================================
# 📁 Diretórios e estrutura de exportação
# ==========================================================
def get_json_export_dir() -> Path:
    """
    Retorna o diretório de exportação de insumos em ambiente seguro.
    Se o diretório padrão não for gravável (como no Streamlit Cloud),
    usa o diretório temporário /tmp.
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
def salvar_insumo(uploaded_file, artefato: str) -> Path:
    """
    Cria um arquivo de metadados JSON básico com informações do upload.
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
    Processa o insumo com IA institucional e salva o resultado como JSON.
    """
    try:
        # Chama o motor IA institucional (SynapseNext v3)
        resultado_ia = processar_insumo_ia(uploaded_file, artefato)

        # Diretório de exportação
        base_dir = get_json_export_dir()
        json_path = base_dir / f"{artefato}_ultimo.json"

        # Registro consolidado
        resultado = {
            "artefato": artefato,
            "arquivo_origem": getattr(uploaded_file, "name", None),
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado_ia": resultado_ia,
        }

        # Escrita robusta do JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"[SynapseNext] JSON salvo em: {json_path}")
        return resultado

    except Exception as e:
        print(f"[ERRO] Falha ao processar insumo: {e}")
        return {"erro": str(e)}


def listar_insumos():
    """
    Lista os arquivos JSON disponíveis no diretório de exportação.
    """
    base_dir = get_json_export_dir()
    arquivos = list(base_dir.glob("*.json"))
    return [f.name for f in arquivos]
