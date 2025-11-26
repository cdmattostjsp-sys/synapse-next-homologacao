# -*- coding: utf-8 -*-
"""
integration_insumos.py – versão estável 2025-D3
Compatível com fluxo DFD / ETP / TR / EDITAL
Ajustado para Streamlit Cloud (leitura via stream /tmp-safe)
"""

from __future__ import annotations

import os
import json
import tempfile
from datetime import datetime

import streamlit as st
import fitz  # PyMuPDF – usado com stream em memória
import docx2txt


# ----------------------------------------------------------
# Detectar tipo de arquivo
# ----------------------------------------------------------
def detectar_tipo(nome: str) -> str:
    """
    Detecta o tipo de arquivo com base na extensão.
    """
    nome = (nome or "").lower()
    if nome.endswith(".pdf"):
        return "pdf"
    if nome.endswith(".docx"):
        return "docx"
    if nome.endswith(".txt"):
        return "txt"
    return "desconhecido"


# ----------------------------------------------------------
# Extração de texto a partir dos bytes do upload
# (sem depender de caminho físico no container)
# ----------------------------------------------------------
def extrair_texto_de_upload(uploaded_file, tipo: str) -> str:
    """
    Recebe o UploadedFile do Streamlit e retorna SEMPRE uma string de texto.
    Em caso de falha, retorna string vazia.
    """
    if uploaded_file is None:
        return ""

    # Lê o conteúdo bruto em memória (bytes)
    try:
        arquivo_bytes = uploaded_file.getvalue()
    except Exception:
        # fallback defensivo
        try:
            arquivo_bytes = uploaded_file.read()
        except Exception:
            return ""

    if not arquivo_bytes:
        return ""

    # ---------------- PDF ----------------
    if tipo == "pdf":
        try:
            texto_paginas = []
            # Leitura via stream (compatível com PyMuPDF >= 1.26.6)
            with fitz.open(stream=arquivo_bytes, filetype="pdf") as pdf:
                for pagina in pdf:
                    texto_paginas.append(pagina.get_text("text"))

            return "\n".join(texto_paginas).strip()
        except Exception as e:
            # Não expõe erro interno ao usuário final; retorna vazio
            # e deixa o fluxo superior tratar como "sem texto suficiente".
            print(f"[integration_insumos] Erro ao extrair texto de PDF via stream: {e}")
            return ""

    # ---------------- DOCX ----------------
    if tipo == "docx":
        try:
            # Usa arquivo temporário em /tmp (mais seguro no Cloud)
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".docx"
            ) as tmp:
                tmp.write(arquivo_bytes)
                tmp_path = tmp.name

            try:
                txt = docx2txt.process(tmp_path)
                return txt if isinstance(txt, str) else ""
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
        except Exception as e:
            print(f"[integration_insumos] Erro ao extrair texto de DOCX: {e}")
            return ""

    # ---------------- TXT ----------------
    if tipo == "txt":
        try:
            return arquivo_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[integration_insumos] Erro ao extrair texto de TXT: {e}")
            return ""

    # Tipo desconhecido
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

    # ---------------------------------------------
    # Validação básica
    # ---------------------------------------------
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
    # Extração de texto diretamente do upload
    # ---------------------------------------------
    texto = extrair_texto_de_upload(uploaded_file, tipo)

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
    # (mantém compatibilidade com DFD e demais módulos)
    # ---------------------------------------------
    base = os.path.join("exports", "insumos", "json")
    try:
        os.makedirs(base, exist_ok=True)
    except Exception as e:
        st.error(f"❌ Falha ao preparar diretório de exportação: {e}")
        return {}

    slug = artefato  # já está em maiúsculas
    arquivo_ultimo = os.path.join(base, f"{slug}_ultimo.json")
    arquivo_ts = os.path.join(
        base, f"{slug}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

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
