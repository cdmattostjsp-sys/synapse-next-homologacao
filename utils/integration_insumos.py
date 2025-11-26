# -*- coding: utf-8 -*-
"""
integration_insumos.py – versão estável 2025-D2
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
# Detectar tipo de arquivo
# ----------------------------------------------------------
def detectar_tipo(nome: str) -> str:
    nome = (nome or "").lower()
    if nome.endswith(".pdf"):
        return "pdf"
    if nome.endswith(".docx"):
        return "docx"
    if nome.endswith(".txt"):
        return "txt"
    return "desconhecido"


# ----------------------------------------------------------
# Extrair texto local (sempre string)
# ----------------------------------------------------------
def extrair_texto_local(caminho: str, tipo: str) -> str:
    """
    SEMPRE retorna string (pode ser vazia).
    Nunca retorna dict nem None.
    """
    if not caminho or not os.path.exists(caminho):
        return ""

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
            with open(caminho, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    return ""


# ----------------------------------------------------------
# Processar insumo (DFD / ETP / TR / EDITAL)
# ----------------------------------------------------------
def processar_insumo(uploaded_file, artefato: str = "DFD") -> dict:
    """
    Processa o arquivo enviado e salva um JSON bruto de insumo em:
      exports/insumos/json/<ARTEFATO>_ultimo.json

    O JSON contém:
      - artefato (DFD / ETP / TR / EDITAL)
      - arquivo (nome original)
      - tipo (pdf / docx / txt)
      - conteudo_textual (texto extraído)
      - data_processamento
    """

    if uploaded_file is None:
        st.warning("Nenhum arquivo enviado.")
        return {}

    artefato = (artefato or "DFD").upper().strip()
    if artefato not in {"DFD", "ETP", "TR", "EDITAL"}:
        # fallback seguro
        artefato = "DFD"

    nome = uploaded_file.name
    tipo = detectar_tipo(nome)

    if tipo == "desconhecido":
        st.error("Formato de arquivo não suportado. Use PDF, DOCX ou TXT.")
        return {}

    st.info(f"📄 Arquivo: **{nome}** — tipo detectado: **{tipo.upper()}**")
    st.caption(f"Artefato de destino selecionado: **{artefato}**")

    # ---------------------------------------------
    # Salvar arquivo físico temporário
    # ---------------------------------------------
    temp_dir = "temp_insumo"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, nome)

    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as e:
        st.error(f"❌ Falha ao salvar arquivo temporário: {e}")
        return {}

    # ---------------------------------------------
    # Extrair texto
    # ---------------------------------------------
    texto = extrair_texto_local(temp_path, tipo)

    if not isinstance(texto, str):
        st.error("❌ Erro interno: a extração de texto não retornou string.")
        return {}

    texto = texto.strip()

    if len(texto) < 20:
        st.error("⚠️ O arquivo não possui texto legível suficiente para processamento.")
        return {}

    # ---------------------------------------------
    # Montar payload padrão de insumo
    # ---------------------------------------------
    payload = {
        "artefato": artefato,
        "arquivo": nome,
        "tipo": tipo,
        "conteudo_textual": texto,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ---------------------------------------------
    # Salvar JSON em exports/insumos/json
    # ---------------------------------------------
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    slug = artefato  # já está em maiúsculas
    arquivo_ultimo = os.path.join(base, f"{slug}_ultimo.json")
    arquivo_ts = os.path.join(base, f"{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arquivo_ts, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo para **{artefato}** processado e salvo com sucesso.")
        st.toast(
            f"💾 Resultado armazenado em exports/insumos/json/ ({slug}_ultimo.json)",
            icon="📁",
        )
        return payload

    except Exception as e:
        st.error(f"❌ Falha ao salvar JSON de insumo: {e}")
        return {}
