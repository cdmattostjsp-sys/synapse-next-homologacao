# -*- coding: utf-8 -*-
"""
utils/integration_tr.py – Exportação/Importação do TR
Responsável por:
- Gravar o arquivo exports/tr_data.json a partir dos metadados do TR.
- Ler o arquivo exports/tr_data.json para pré-preencher o módulo Contrato.
"""

import json
import os
from typing import Dict, Any

EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
TR_JSON_PATH = os.path.join(EXPORTS_DIR, "tr_data.json")


def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    os.makedirs(path, exist_ok=True)


def export_tr_to_json(data: Dict[str, Any], path: str = TR_JSON_PATH) -> str:
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_tr_from_json(path: str = TR_JSON_PATH) -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# ==========================================================
# 🤖 Análise Semântica de Insumo (IA Institucional – TR)
# ==========================================================

import re, json
from pathlib import Path
from utils.ai_client import AIClient

client = AIClient()

def ler_modelos_tr():
    """Lê a base de conhecimento institucional (Knowledge Base) para TR."""
    base = Path(__file__).resolve().parents[1] / "knowledge" / "tr_models"
    textos = []
    if base.exists():
        for arq in base.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)


def processar_insumo_tr(arquivo, artefato: str = "TR") -> dict:
    """
    Extrai o texto do arquivo enviado (PDF, DOCX ou TXT),
    realiza análise semântica institucional e retorna um dicionário
    com os campos padronizados do Termo de Referência (TR).
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
    modelos = ler_modelos_tr()

    # 2️⃣ Prompt institucional
    system_prompt = (
        "Você é um agente institucional especializado em Termo de Referência (TR). "
        "Analise o texto do insumo e extraia, em formato JSON, os campos padronizados "
        "de um TR conforme o padrão da Secretaria de Administração e Abastecimento (TJSP)."
    )

    user_prompt = f"""
Texto do insumo:
\"\"\"{texto_limpo}\"\"\"

Modelos institucionais de referência:
\"\"\"{modelos}\"\"\"

Retorne apenas um JSON com os seguintes campos:
- objeto
- justificativa
- especificacoes_tecnicas
- criterios_de_julgamento
- obrigacoes_da_contratada
- prazo_execucao
- estimativa_valor
- fonte_recurso
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

    print(f"[IA:TR] Arquivo: {arquivo.name} – Campos: {list(campos.keys())}")
    return {
        "artefato": artefato,
        "nome_arquivo": arquivo.name,
        "status": "processado",
        "campos_ai": campos
    }
