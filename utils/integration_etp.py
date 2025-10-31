# -*- coding: utf-8 -*-
"""
utils/integration_etp.py – Exportação/Importação do ETP
Responsável por:
- Gravar o arquivo exports/etp_data.json a partir dos metadados do ETP.
- Ler o arquivo exports/etp_data.json para pré-preencher o módulo TR.
"""

import json
import os
import re
from typing import Dict, Any
from pathlib import Path
from utils.ai_client import AIClient

# ==========================================================
# 📂 Diretórios e caminhos de exportação
# ==========================================================
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
ETP_JSON_PATH = os.path.join(EXPORTS_DIR, "etp_data.json")
client = AIClient()

# ==========================================================
# 📤 Funções utilitárias
# ==========================================================
def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    os.makedirs(path, exist_ok=True)

def export_etp_to_json(data: Dict[str, Any], path: str = ETP_JSON_PATH) -> str:
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load_etp_from_json(path: str = ETP_JSON_PATH) -> Dict[str, Any]:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# ==========================================================
# 🧠 Base de conhecimento institucional (ETP)
# ==========================================================
def ler_modelos_etp() -> str:
    """Lê a base de conhecimento institucional (Knowledge Base) para ETP."""
    base = Path(__file__).resolve().parents[1] / "knowledge" / "etp_models"
    textos = []
    if base.exists():
        for arq in base.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)

# ==========================================================
# 🤖 Processamento de Insumo – ETP
# ==========================================================
def processar_insumo_etp(arquivo, artefato: str = "ETP") -> dict:
    """
    Extrai o texto do arquivo enviado (PDF, DOCX ou TXT),
    realiza análise semântica institucional e retorna campos estruturados.
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
    modelos = ler_modelos_etp()

    # 2️⃣ Prompt institucional
    system_prompt = (
        "Você é um agente institucional especializado em Estudo Técnico Preliminar (ETP). "
        "Analise o texto do insumo e extraia os campos padronizados conforme o modelo do TJSP."
    )

    user_prompt = f"""
Texto do insumo:
\"\"\"{texto_limpo}\"\"\"

Modelos institucionais de referência:
\"\"\"{modelos}\"\"\"

Retorne apenas um JSON com os seguintes campos:
- objeto
- problema_a_resolver
- solucao_proposta
- alternativas_analisadas
- justificativa_da_escolha
- resultados_esperados
- impacto_orcamentario
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

    # ==========================================================
    # 🔄 Normalização dos campos para compatibilidade com o front-end
    # ==========================================================
    campos_ai = {
        "requisitos": campos.get("solucao_proposta", campos.get("objeto", "")),
        "custos": campos.get("impacto_orcamentario", "A definir com base no orçamento institucional."),
        "riscos": campos.get("problema_a_resolver", "Sem riscos relevantes identificados."),
        "responsavel_tecnico": campos.get("responsavel_tecnico", "Responsável técnico a designar.")
    }

    # Garante que nenhum campo fique vazio
    for k, v in campos_ai.items():
        if not v:
            campos_ai[k] = "—"

    print(f"[IA:ETP] Arquivo: {arquivo.name} – Campos normalizados: {list(campos_ai.keys())}")

    # ==========================================================
    # 📦 Retorno final compatível com SynapseNext
    # ==========================================================
    return {
        "artefato": artefato,
        "nome_arquivo": arquivo.name,
        "status": "processado",
        "campos_ai": campos_ai
    }
