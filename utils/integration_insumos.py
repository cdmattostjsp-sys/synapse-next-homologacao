# -*- coding: utf-8 -*-
"""
integration_insumos.py – versão estável 2025 (multi-artefato)
Compatível com fluxo DFD / ETP / TR / EDITAL
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
    """
    SEMPRE retorna string.
    Nunca retorna dict.
    """

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
        except Exception:
            return ""

    return ""


# ----------------------------------------------------------
# Processar insumo
# ----------------------------------------------------------
def processar_insumo(uploaded_file, artefato: str = "DFD") -> dict:
    """
    Processa um arquivo de insumo (PDF / DOCX / TXT) e salva o texto
    em exports/insumos/json/<ARTEFATO>_ultimo.json.

    artefato: "DFD", "ETP", "TR", "EDITAL" etc.
    """
    if uploaded_file is None:
        st.warning("Nenhum arquivo enviado.")
        return {}

    artefato = (artefato or "DFD").upper()

    nome = uploaded_file.name
    tipo = detectar_tipo(nome)

    if tipo == "desconhecido":
        st.error("Formato não suportado. Use PDF, DOCX ou TXT.")
        return {}

    st.info(f"📄 Tipo detectado: **{tipo.upper()}** (artefato: {artefato})")

    # -------------------------------
    # Salvar arquivo em temp_insumo
    # -------------------------------
    temp_dir = "temp_insumo"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, nome)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # -------------------------------
    # Extrair texto
    # -------------------------------
    texto = extrair_texto_local(temp_path, tipo)

    if not isinstance(texto, str):
        st.error("Erro interno: extração não retornou texto.")
        return {}

    texto = texto.strip()

    if len(texto) < 20:
        st.error("O arquivo não possui texto legível suficiente para processamento.")
        return {}

    # -------------------------------
    # Montar payload genérico
    # -------------------------------
    payload = {
        "artefato": artefato,
        "arquivo": nome,
        "tipo": tipo,
        "conteudo_textual": texto,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # -------------------------------
    # Salvar JSON por artefato
    # -------------------------------
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    # Ex.: DFD_ultimo.json, ETP_ultimo.json, TR_ultimo.json...
    arquivo_ultimo = os.path.join(base, f"{artefato}_ultimo.json")
    arquivo_historico = os.path.join(
        base,
        f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    )

    try:
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arquivo_historico, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo para o artefato {artefato} processado com sucesso!")
        st.caption(f"💾 Arquivo salvo em: {arquivo_ultimo}")

        return payload

    except Exception as e:
        st.error(f"❌ Falha ao salvar JSON de insumo para {artefato}: {e}")
        return {}
