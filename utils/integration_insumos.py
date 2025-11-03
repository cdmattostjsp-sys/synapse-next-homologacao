# ==========================================================
# utils/integration_insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Integração híbrida entre o motor original de insumos e o motor IA institucional v3
# ==========================================================

import streamlit as st
import os
import io
import json
from datetime import datetime
from utils.integration_ai_engine import processar_insumo as processar_insumo_ia

# ==========================================================
# 🧠 Função principal – processamento de insumo
# ==========================================================
def processar_insumo(uploaded_file, artefato: str):
    """
    Processa insumos institucionais e encaminha o resultado ao módulo correspondente.
    Compatível com DFD, ETP, TR e Edital.
    Integra-se ao motor IA institucional v3 e mantém persistência entre páginas.
    """

    if not uploaded_file:
        st.warning("Nenhum arquivo foi enviado.")
        return None

    artefato = artefato.upper().strip()
    nome_arquivo = uploaded_file.name

    # ==========================================================
    # 📄 Extração inicial de texto (não exibe logs na UI)
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
    except Exception as e:
        st.error(f"Erro ao extrair texto: {e}")

    # ==========================================================
    # 🤖 Aciona o motor IA institucional v3
    # ==========================================================
    try:
        resultado_ia = processar_insumo_ia(
            uploaded_file,
            tipo_artefato=artefato,
            metadados_form={"origem": "integration_insumos.py", "arquivo": nome_arquivo},
            filename=nome_arquivo,
        )
        campos_norm = resultado_ia.get("campos", {})
    except Exception as e:
        st.error(f"Falha no motor IA institucional v3: {e}")
        campos_norm = {}

    # ==========================================================
    # 💾 Monta payload final
    # ==========================================================
    payload = {
        "nome_arquivo": nome_arquivo,
        "artefato": artefato,
        "texto": texto_extraido[:8000],
        "campos_ai": campos_norm,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ==========================================================
    # 🧭 Atualiza sessão ativa (Streamlit)
    # ==========================================================
    key_map = {
        "DFD": "dfd_campos_ai",
        "ETP": "etp_campos_ai",
        "TR": "tr_campos_ai",
        "EDITAL": "edital_campos_ai",
    }
    key_last = f"last_insumo_{artefato.lower()}"
    st.session_state[key_map.get(artefato, f"{artefato.lower()}_campos_ai")] = campos_norm
    st.session_state[key_last] = payload

    # ==========================================================
    # 🧱 Persistência em disco (para fallback entre páginas)
    # ==========================================================
    EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")
    os.makedirs(EXPORTS_JSON_DIR, exist_ok=True)

    # Salva backup histórico e último ativo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_historico = os.path.join(EXPORTS_JSON_DIR, f"{artefato}_{timestamp}.json")
    arquivo_ultimo = os.path.join(EXPORTS_JSON_DIR, f"{artefato}_ultimo.json")

    try:
        with open(arquivo_historico, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"⚠️ Falha ao salvar JSON: {e}")

    st.success(f"Insumo para {artefato} processado e salvo com sucesso.")
    return payload
