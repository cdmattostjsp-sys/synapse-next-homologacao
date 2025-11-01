# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Funções de integração entre insumos e módulos (DFD, ETP, TR, Edital)
# com extração textual, IA institucional e persistência local
# ==========================================================

import streamlit as st
import os
import io
import json
from datetime import datetime

# ==========================================================
# 🧠 Função principal – processamento dinâmico de insumo
# ==========================================================

def processar_insumo(uploaded_file, artefato: str):
    """
    Processa insumos institucionais e os encaminha ao módulo correspondente.
    Compatível com DFD, ETP, TR e Edital.
    """

    if not uploaded_file:
        st.warning("Nenhum arquivo foi enviado.")
        return None

    artefato = artefato.upper().strip()
    nome_arquivo = uploaded_file.name
    st.info(f"📄 Processando insumo '{nome_arquivo}' para o módulo {artefato}...")

    # ==========================================================
    # 📂 Leitura segura de arquivo (TXT, DOCX, PDF)
    # ==========================================================
    extensao = os.path.splitext(nome_arquivo)[1].lower()
    texto_extraido = ""

    try:
        if extensao == ".txt":
            texto_extraido = uploaded_file.read().decode("utf-8", errors="ignore")

        elif extensao == ".docx":
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.read()))
            texto_extraido = "\n".join([p.text for p in doc.paragraphs])

        elif extensao == ".pdf":
            from PyPDF2 import PdfReader
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
            texto_extraido = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])

        else:
            texto_extraido = "⚠️ Formato de arquivo não suportado para extração de texto."

    except Exception as e:
        st.error(f"Erro ao extrair texto do arquivo: {e}")
        texto_extraido = ""

    # ==========================================================
    # 🤖 Extração semântica com IA institucional (OpenAI)
    # ==========================================================
    campos_norm = {}
    try:
        from openai import OpenAI

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
        if not OPENAI_API_KEY:
            raise ValueError("Chave da API OpenAI não configurada (OPENAI_API_KEY).")

        client = OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"""
Você é um redator institucional do Tribunal de Justiça de São Paulo (SAAB/TJSP).
Sua função é analisar o conteúdo abaixo e devolver um resumo estruturado
nos moldes de documentos administrativos oficiais.

INSTRUÇÕES:
- Mantenha o tom formal, técnico e redacional compatível com documentos do TJSP.
- Preencha todos os campos solicitados, mesmo que parcialmente inferidos.
- Retorne APENAS um JSON válido, no formato:

{{
  "unidade_solicitante": "...",
  "responsavel_tecnico": "...",
  "objeto": "...",
  "justificativa_tecnica": "...",
  "criterios_julgamento": "...",
  "riscos": "...",
  "prazo_execucao": "...",
  "estimativa_valor": "...",
  "fonte_recurso": "..."
}}

CONTEÚDO EXTRAÍDO ({artefato}):
\"\"\"{texto_extraido[:6000]}\"\"\"
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista institucional do TJSP, especialista em artefatos administrativos.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.25,
        )

        conteudo_ia = response.choices[0].message.content.strip()
        campos_norm = json.loads(conteudo_ia)

        st.success("✅ Conteúdo processado com IA institucional.")

    except Exception as e:
        st.warning(f"⚠️ Falha ao gerar campos com IA institucional ({e}). Usando preenchimento padrão.")
        campos_norm = {
            "objeto": f"Objeto identificado a partir do insumo '{uploaded_file.name}'",
            "unidade_solicitante": "Departamento de Administração e Planejamento",
            "responsavel_tecnico": "Responsável Institucional (IA)",
            "justificativa_tecnica": "Justificativa técnica preliminar extraída automaticamente.",
            "criterios_julgamento": "Menor preço global.",
            "riscos": "Risco operacional moderado.",
            "prazo_execucao": "90 dias",
            "estimativa_valor": "R$ 150.000,00",
            "fonte_recurso": "Orçamento ordinário TJSP",
        }

    # ==========================================================
    # 💾 Monta payload final
    # ==========================================================
    payload = {
        "nome_arquivo": uploaded_file.name,
        "artefato": artefato,
        "texto": texto_extraido[:8000],
        "campos_ai": campos_norm,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ==========================================================
    # 🧭 Atualiza sessão ativa (Streamlit)
    # ==========================================================
    if artefato == "DFD":
        st.session_state["dfd_campos_ai"] = campos_norm
        st.session_state["last_insumo_dfd"] = payload
    elif artefato == "ETP":
        st.session_state["etp_campos_ai"] = campos_norm
        st.session_state["last_insumo_etp"] = payload
    elif artefato == "TR":
        st.session_state["tr_campos_ai"] = campos_norm
        st.session_state["last_insumo_tr"] = payload
    elif artefato == "EDITAL":
        st.session_state["edital_campos_ai"] = campos_norm
        st.session_state["last_insumo_edital"] = payload

    # ==========================================================
    # 📦 Exportação de backup em JSON
    # ==========================================================
    EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")
    os.makedirs(EXPORTS_JSON_DIR, exist_ok=True)

    arquivo_saida = os.path.join(
        EXPORTS_JSON_DIR, f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    try:
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Não foi possível salvar o JSON: {e}")

    # ==========================================================
    # ✅ Retorno final
    # ==========================================================
    st.success(f"Insumo '{artefato}' processado e encaminhado com sucesso ao respectivo módulo.")
    return payload
