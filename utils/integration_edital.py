# ==============================================
# utils/integration_edital.py – SynapseNext / SAAB TJSP
# ==============================================
import os
import json
import fitz  # PyMuPDF
import docx2txt
from openai import OpenAI
from io import BytesIO
from datetime import datetime

# ==============================================
# 🔧 Inicialização
# ==============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# ==============================================
# 📘 Leitura e extração de texto
# ==============================================
def extrair_texto(arquivo):
    nome = arquivo.name.lower()

    if nome.endswith(".pdf"):
        texto = ""
        with fitz.open(stream=arquivo.read(), filetype="pdf") as pdf:
            for pagina in pdf:
                texto += pagina.get_text("text") + "\n"
        return texto

    elif nome.endswith(".docx"):
        temp_path = f"/tmp/{arquivo.name}"
        with open(temp_path, "wb") as tmp:
            tmp.write(arquivo.getvalue())
        return docx2txt.process(temp_path)

    elif nome.endswith(".txt"):
        return arquivo.read().decode("utf-8")

    else:
        return ""

# ==============================================
# 🧠 Processamento semântico com IA institucional
# ==============================================
def processar_insumo_edital(arquivo, contexto_previo=None):
    """
    Processa um insumo (PDF/DOCX/TXT) e gera campos estruturados para o Edital.
    Caso exista contexto de DFD/ETP/TR, realiza fusão semântica controlada.
    """
    try:
        texto_insumo = extrair_texto(arquivo)
        nome_arquivo = arquivo.name

        prompt_base = f"""
Você é um assistente institucional do Tribunal de Justiça de São Paulo (TJSP),
especializado em elaboração e consolidação de minutas de Edital de Licitação.
Analise o documento fornecido e identifique os campos-chave.

Documento do insumo:
\"\"\"{texto_insumo[:4000]}\"\"\"

Retorne os dados no seguinte formato JSON:
{{
  "unidade_solicitante": "",
  "responsavel_tecnico": "",
  "objeto": "",
  "modalidade": "",
  "regime_execucao": "",
  "base_legal": "",
  "criterios_julgamento": "",
  "prazo_execucao": "",
  "forma_pagamento": "",
  "penalidades": "",
  "observacoes_finais": ""
}}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um analista técnico do TJSP responsável por estruturar artefatos de licitação de acordo com a SAAB."},
                {"role": "user", "content": prompt_base},
            ],
            temperature=0.2,
        )

        campos_extraidos = response.choices[0].message.content.strip()
        try:
            campos_ai = json.loads(campos_extraidos)
        except json.JSONDecodeError:
            campos_ai = {"objeto": texto_insumo[:1000]}

        # =======================================================
        # 🔗 Fusão semântica com contexto prévio (DFD/ETP/TR)
        # =======================================================
        if contexto_previo and isinstance(contexto_previo, dict):
            for chave, valor in contexto_previo.items():
                if chave not in campos_ai or not campos_ai[chave].strip():
                    campos_ai[chave] = valor

        resultado = {
            "artefato": "EDITAL",
            "nome_arquivo": nome_arquivo,
            "status": "processado",
            "campos_ai": campos_ai
        }

        return resultado

    except Exception as e:
        return {"erro": f"Falha ao processar o insumo do Edital: {e}"}

# ==============================================
# 🧩 Função pública de integração
# ==============================================
def integrar_com_contexto(session_state):
    """
    Combina os dados prévios de DFD, ETP e TR para gerar contexto cumulativo.
    """
    contexto = {}
    for chave in ["dfd_campos_ai", "etp_campos_ai", "tr_campos_ai"]:
        if chave in session_state and isinstance(session_state[chave], dict):
            contexto.update(session_state[chave])
    return contexto
