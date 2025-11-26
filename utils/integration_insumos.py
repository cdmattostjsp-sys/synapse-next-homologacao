# -*- coding: utf-8 -*-
"""
integration_insumos.py – versão estável 2025
Compatível com fluxo DFD/ETP/TR/EDITAL
"""

from __future__ import annotations
import os
import json
import streamlit as st
from datetime import datetime

from utils.parser_pdf import extract_text_from_pdf
import docx2txt


# ----------------------------------------------------------
# Detectar tipo
# ----------------------------------------------------------
def detectar_tipo(nome: str) -> str:
    nome = nome.lower()
    if nome.endswith(".pdf"):
        return "pdf"
    if nome.endswith(".docx"):
        return "docx"
    if nome.endswith(".txt"):
        return "txt"
    return "desconhecido"


# ----------------------------------------------------------
# Extrair texto local
# ----------------------------------------------------------
def extrair_texto_local(caminho: str, tipo: str) -> str:
    """ Sempre retorna string. Nunca dict. """

    if tipo == "pdf":
        try:
            txt = extract_text_from_pdf(caminho)
            return txt if isinstance(txt, str) else ""
        except Exception:
            return ""

    if tipo == "docx":
        try:
            txt = docx2txt.process(caminho)
            return txt if isinstance(txt, str) else ""
        except Exception:
            return ""

    if tipo == "txt":
        try:
            return open(caminho, "r", encoding="utf-8").read()
        except:
            return ""

    return ""


# ----------------------------------------------------------
# Processar Insumo (corrigido)
# ----------------------------------------------------------
def processar_insumo(uploaded_file, artefato="DFD"):
    """
    Processa o insumo e salva no JSON correto:

    DFD  → DFD_ultimo.json
    ETP  → ETP_ultimo.json
    TR   → TR_ultimo.json
    EDITAL → EDITAL_ultimo.json
    """

    if uploaded_file is None:
        st.warning("Nenhum arquivo enviado.")
        return {}

    artefato = artefato.upper().strip()

    nome = uploaded_file.name
    tipo = detectar_tipo(nome)

    if tipo == "desconhecido":
        st.error("Formato não suportado.")
        return {}

    st.info(f"📄 Tipo detectado: **{tipo.upper()}**")

    # Salvar arquivo temporário
    temp_dir = "temp_insumo"
    os.makedirs(temp_dir, exist_ok=True)

    temp_path = os.path.join(temp_dir, nome)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extrair texto puro
    texto = extrair_texto_local(temp_path, tipo)

    if not isinstance(texto, str):
        st.error("Erro interno: extração não retornou texto.")
        return {}

    texto = texto.strip()

    if len(texto) < 20:
        st.error("O arquivo não possui texto legível.")
        return {}

    # Payload básico
    payload = {
        "arquivo": nome,
        "tipo": tipo,
        "conteudo_textual": texto,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ----------------------------------------------
    # SALVAR no arquivo correto (correção principal)
    # ----------------------------------------------
    base = "exports/insumos/json"
    os.makedirs(base, exist_ok=True)

    arquivo_final = os.path.join(base, f"{artefato}_ultimo.json")
    arquivo_timestamp = os.path.join(
        base, f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    try:
        # Arquivo principal
        with open(arquivo_final, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # Arquivo histórico
        with open(arquivo_timestamp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo processado e encaminhado para {artefato}!")
        return payload

    except Exception as e:
        st.error(f"❌ Falha ao salvar insumo: {e}")
        return {}
