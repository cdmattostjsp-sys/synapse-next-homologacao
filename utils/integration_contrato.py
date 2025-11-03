# -*- coding: utf-8 -*-
# ==========================================================
# utils/integration_contrato.py – SynapseNext / SAAB TJSP
# ==========================================================
# - Processa insumos (PDF/DOCX/TXT) para CONTRATO com IA institucional
# - Normaliza campos para o formulário do módulo Contrato
# - Exporta/Carrega JSON em exports/contrato_data.json
# - Permite fusão de contexto com DFD/ETP/TR/Edital
# ==========================================================

import os
import re
import json
from io import BytesIO
from typing import Dict, Any
from pathlib import Path

import docx2txt
import fitz  # PyMuPDF
from openai import OpenAI

# -----------------------------
# ⚙️ OpenAI Client
# -----------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# 📂 Export paths
# -----------------------------
EXPORTS_DIR = Path(__file__).resolve().parents[1] / "exports"
CONTRATO_JSON_PATH = EXPORTS_DIR / "contrato_data.json"

# -----------------------------
# 📚 Knowledge Base (Contrato)
# -----------------------------
def ler_modelos_contrato() -> str:
    base = Path(__file__).resolve().parents[1] / "knowledge" / "contrato_models"
    textos = []
    if base.exists():
        for arq in base.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)

# -----------------------------
# 🧰 Utilitários Export/Load
# -----------------------------
def ensure_exports_dir():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def export_contrato_to_json(data: Dict[str, Any], path: Path = CONTRATO_JSON_PATH) -> str:
    ensure_exports_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(path)

def load_contrato_from_json(path: Path = CONTRATO_JSON_PATH) -> Dict[str, Any]:
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# -----------------------------
# 🧾 Extração de texto
# -----------------------------
def _extrair_texto_arquivo(arquivo) -> str:
    nome = getattr(arquivo, "name", "").lower()
    try:
        if nome.endswith(".pdf"):
            dados = arquivo.read()
            arquivo.seek(0)
            texto = ""
            with fitz.open(stream=dados, filetype="pdf") as pdf:
                for p in pdf:
                    texto += p.get_text("text") + "\n"
            return re.sub(r"\s+", " ", texto).strip()

        if nome.endswith(".docx"):
            dados = arquivo.read()
            arquivo.seek(0)
            return re.sub(r"\s+", " ", docx2txt.process(BytesIO(dados))).strip()

        if nome.endswith(".txt"):
            dados = arquivo.read()
            arquivo.seek(0)
            return re.sub(r"\s+", " ", dados.decode("utf-8", errors="ignore")).strip()
    except Exception:
        pass
    return ""

# -----------------------------
# 🔗 Fusão de contexto cumulativo
# -----------------------------
def integrar_com_contexto(session_state: Dict[str, Any]) -> Dict[str, Any]:
    """Mescla DFD + ETP + TR + Edital para enriquecer CONTRATO."""
    contexto = {}
    for chave in ["dfd_campos_ai", "etp_campos_ai", "tr_campos_ai", "edital_campos_ai"]:
        bloco = session_state.get(chave)
        if isinstance(bloco, dict):
            contexto.update(bloco)
    return contexto

# -----------------------------
# 🤖 Processamento IA – CONTRATO
# -----------------------------
def processar_insumo_contrato(arquivo, artefato: str = "CONTRATO", contexto_previo: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Lê arquivo (PDF/DOCX/TXT), consulta modelos institucionais e retorna
    campos normalizados para o formulário do módulo CONTRATO.
    """
    texto = _extrair_texto_arquivo(arquivo)
    if not texto:
        return {"erro": "Falha na extração do texto do insumo de CONTRATO."}

    modelos = ler_modelos_contrato()

    system_prompt = (
        "Você é um redator institucional do Tribunal de Justiça de São Paulo (SAAB/TJSP), "
        "especializado na elaboração de contratos administrativos alinhados à Lei 14.133/2021."
    )

    # Contexto prévio ajuda a IA quando o insumo é enxuto
    contexto_json = json.dumps(contexto_previo or {}, ensure_ascii=False, indent=2)

    user_prompt = f"""
Você receberá o conteúdo de um insumo (rascunho, minuta ou informações correlatas) e opcionalmente um contexto
com metadados provenientes de DFD/ETP/TR/Edital. Retorne APENAS um JSON com os campos do contrato:

Campos desejados (JSON):
{{
  "objeto": "",
  "partes": "",
  "vigencia": "",
  "valor_global": "",
  "reajuste": "",
  "garantias": "",
  "prazos_pagamento": "",
  "obrigacoes_contratada": "",
  "obrigacoes_contratante": "",
  "fiscalizacao": "",
  "penalidades": "",
  "rescisao": "",
  "foro": ""
}}

Contexto prévio (caso exista):
{contexto_json}

Texto do insumo:
\"\"\"{texto[:8000]}\"\"\"
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        conteudo = resp.choices[0].message.content.strip()
        # Extrai JSON
        match = re.search(r"\{.*\}", conteudo, re.DOTALL)
        campos = json.loads(match.group(0)) if match else {"objeto": texto[:1000]}
    except Exception as e:
        campos = {"erro": f"Falha ao processar IA de CONTRATO: {e}"}

    # -----------------------------
    # 🔄 Normalização/Defaults
    # -----------------------------
    defaults = {
        "objeto": "",
        "partes": "",
        "vigencia": "",
        "valor_global": "",
        "reajuste": "Conforme índice oficial aplicável e cláusulas da Lei 14.133/2021.",
        "garantias": "",
        "prazos_pagamento": "Conforme cronograma e liquidação de despesa.",
        "obrigacoes_contratada": "",
        "obrigacoes_contratante": "",
        "fiscalizacao": "Fiscal do contrato a ser designado pela unidade competente.",
        "penalidades": "",
        "rescisao": "",
        "foro": "Comarca de São Paulo/SP.",
    }
    campos_ai = {k: (campos.get(k) or defaults.get(k) or "—") for k in defaults.keys()}

    print(f"[IA:CONTRATO] Arquivo: {getattr(arquivo,'name','(sem nome)')} – Campos: {list(campos_ai.keys())}")

    return {
        "artefato": artefato,
        "nome_arquivo": getattr(arquivo, "name", ""),
        "status": "processado",
        "campos_ai": campos_ai,
    }
