# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão Engenheiro Synapse – vNext_2025.11.07
# ==========================================================

import os
import json
import tempfile
from datetime import datetime
from pathlib import Path

import fitz  # ✅ PyMuPDF – leitura via stream
from utils.ai_client import AIClient  # ✅ Cliente institucional OpenAI

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
    Processa o insumo PDF:
      1. Lê o PDF via stream (PyMuPDF)
      2. Extrai o texto integral
      3. Chama o cliente institucional de IA
      4. Gera e salva o JSON final em exports/insumos/json
    """
    try:
        # ==========================================================
        # 1️⃣ Leitura do PDF via stream – compatível com PyMuPDF==1.26.6
        # ==========================================================
        with fitz.open(stream=uploaded_file.getvalue(), filetype="pdf") as doc:
            texto_extraido = ""
            for pagina in doc:
                texto_extraido += pagina.get_text("text")

        print("[SynapseNext] Texto extraído com sucesso ✅")

        # ==========================================================
        # 2️⃣ Chamada da IA institucional (via utils/ai_client.py)
        # ==========================================================
        ai = AIClient()
        prompt_base = f"Analise o documento de {artefato} e gere estrutura JSON."
        resposta_ia = ai.ask(prompt=prompt_base, conteudo=texto_extraido, artefato=artefato)

        print("[SynapseNext] Chamando IA institucional... 🧠")

        # ==========================================================
        # 3️⃣ Montagem do registro consolidado e exportação
        # ==========================================================
        base_dir = get_json_export_dir()
        json_path = base_dir / f"{artefato}_ultimo.json"

        resultado = {
            "artefato": artefato,
            "arquivo_origem": getattr(uploaded_file, "name", None),
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "texto_extraido": texto_extraido[:1000],  # preview para auditoria
            "resultado_ia": resposta_ia,
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"[SynapseNext] JSON gerado e salvo em: {json_path} 💾")
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
