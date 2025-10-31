# -*- coding: utf-8 -*-
"""
utils/integration_dfd.py – Exportação/Importação e Análise Semântica do DFD

Responsável por:
1. Gravar e ler o arquivo exports/dfd_data.json (integração com ETP).
2. Analisar semanticamente insumos (PDF/DOCX/TXT) para preencher o DFD.
"""

from __future__ import annotations
import json, os, re
from typing import Dict, Any
from pathlib import Path

# ==========================================================
# 🔧 Funções de exportação / importação JSON
# ==========================================================

EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
DFD_JSON_PATH = os.path.join(EXPORTS_DIR, "dfd_data.json")

def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    """Garante que o diretório de exportação exista."""
    os.makedirs(path, exist_ok=True)

def export_dfd_to_json(data: Dict[str, Any], path: str = DFD_JSON_PATH) -> str:
    """Salva metadados do DFD (dict) em JSON UTF-8. Retorna o caminho salvo."""
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load_dfd_from_json(path: str = DFD_JSON_PATH) -> Dict[str, Any]:
    """Lê o arquivo JSON se existir; caso contrário, retorna {}."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# ==========================================================
# 🤖 Análise Semântica de Insumo (IA Institucional)
# ==========================================================

from utils.ai_client import AIClient
client = AIClient()

def ler_modelos_dfd():
    """Lê modelos de referência institucional (Knowledge Base)"""
    base = Path(__file__).resolve().parents[1] / "knowledge" / "dfd_models"
    textos = []
    if base.exists():
        for arq in base.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)

def processar_insumo(arquivo, artefato: str = "DFD") -> dict:
    """
    Extrai texto de insumo PDF/DOCX/TXT e realiza análise semântica institucional
    para preenchimento automático do Documento de Formalização da Demanda (DFD).
    """
    from io import BytesIO
    import fitz, docx2txt

    dados = arquivo.read()
    arquivo.seek(0)
    nome = arquivo.name.lower()
    texto_extraido = ""

    # 1️⃣ Extração de texto
    try:
        if nome.endswith(".pdf"):
            pdf = fitz.open(stream=dados, filetype="pdf")
            texto_extraido = "".join(p.get_text() for p in pdf)
        elif nome.endswith(".docx"):
            texto_extraido = docx2txt.process(BytesIO(dados))
        elif nome.endswith(".txt"):
            texto_extraido = dados.decode("utf-8", errors="ignore")
    except Exception as e:
        return {"erro": f"Falha ao extrair texto: {e}"}

    if not texto_extraido.strip():
        return {"erro": "Texto vazio após leitura do insumo."}

    texto_limpo = re.sub(r"\s+", " ", texto_extraido).strip()
    modelos = ler_modelos_dfd()

    # 2️⃣ Prompt institucional
    system_prompt = (
        "Você é um agente institucional do Tribunal de Justiça de São Paulo, "
        "especializado em analisar documentos administrativos e extrair informações "
        "para preencher um Documento de Formalização da Demanda (DFD)."
    )

    user_prompt = f"""
Texto do insumo:
\"\"\"{texto_limpo}\"\"\"

Modelos institucionais de referência:
\"\"\"{modelos}\"\"\"

Retorne apenas um JSON com os seguintes campos:
- unidade_solicitante
- responsavel
- objeto
- justificativa
- quantidade
- urgencia
- riscos
- alinhamento_planejamento
"""

    # 3️⃣ Chamada à IA institucional
    try:
        response = client.chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        conteudo = response["content"]
        match = re.search(r"\{.*\}", conteudo, re.DOTALL)
        campos = json.loads(match.group(0)) if match else {"objeto": texto_limpo[:800]}
    except Exception as e:
        campos = {"erro": f"Falha ao processar IA: {e}"}

    print(f"[IA:DFD] Arquivo: {arquivo.name} – Campos: {list(campos.keys())}")
    return {
        "artefato": artefato,
        "nome_arquivo": arquivo.name,
        "status": "processado",
        "campos_ai": campos
    }
