# -*- coding: utf-8 -*-
"""
integration_insumos.py – versão estável 2025-D4 (FINAL)
Compatível com DFD/ETP/TR/Edital – Pipeline Moderno 2025
Ajustado para Python 3.13 + PyMuPDF 1.25.1 + Streamlit Cloud
"""

from __future__ import annotations

import os
import json
import tempfile
from datetime import datetime

import streamlit as st
import fitz           # PyMuPDF
import docx2txt


# ==========================================================
# Detectar tipo de arquivo
# ==========================================================
def detectar_tipo(nome: str) -> str:
    nome = (nome or "").lower()
    if nome.endswith(".pdf"):
        return "pdf"
    if nome.endswith(".docx"):
        return "docx"
    if nome.endswith(".txt"):
        return "txt"
    return "desconhecido"


# ==========================================================
# Extração de texto do upload – versão segura 2025-D4
# ==========================================================
def extrair_texto_de_upload(uploaded_file, tipo: str) -> str:
    """
    Retorna SEMPRE uma string.
    """

    if uploaded_file is None:
        return ""

    # bytes do upload
    try:
        arquivo_bytes = uploaded_file.getvalue()
    except:
        try:
            arquivo_bytes = uploaded_file.read()
        except:
            return ""

    if not arquivo_bytes:
        return ""

    # ---------------- PDF ----------------
    if tipo == "pdf":
        try:
            texto = []

            # tentativa principal (PyMuPDF 1.25)
            try:
                doc = fitz.open(stream=arquivo_bytes, filetype="pdf")
            except:
                # fallback legacy
                doc = fitz.open("pdf", arquivo_bytes)

            for pagina in doc:
                texto.append(pagina.get_text("text"))

            return "\n".join(texto).strip()

        except Exception as e:
            print(f"[integration_insumos][PDF] erro: {e}")
            return ""

    # ---------------- DOCX ----------------
    if tipo == "docx":
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(arquivo_bytes)
                caminho = tmp.name

            try:
                txt = docx2txt.process(caminho)
                return txt if isinstance(txt, str) else ""
            finally:
                try:
                    os.unlink(caminho)
                except:
                    pass

        except Exception as e:
            print(f"[integration_insumos][DOCX] erro: {e}")
            return ""

    # ---------------- TXT ----------------
    if tipo == "txt":
        try:
            return arquivo_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"[integration_insumos][TXT] erro: {e}")
            return ""

    return ""


# ==========================================================
# Processamento principal
# ==========================================================
def processar_insumo(uploaded_file, artefato: str = "DFD") -> dict:
    """
    Extrai texto, monta payload Moderno 2025 e grava:
       exports/insumos/json/<ARTEFATO>_ultimo.json
    """

    if uploaded_file is None:
        st.warning("Nenhum arquivo enviado.")
        return {}

    artefato = (artefato or "DFD").upper().strip()
    if artefato not in {"DFD", "ETP", "TR", "EDITAL", "CONTRATO"}:
        artefato = "DFD"

    nome = uploaded_file.name
    tipo = detectar_tipo(nome)

    if tipo == "desconhecido":
        st.error("Formato não suportado. Use PDF, DOCX ou TXT.")
        return {}

    st.info(f"📄 Arquivo recebido: {nome} (tipo detectado: {tipo})")

    # =======================
    # Extração do texto
    # =======================
    texto = extrair_texto_de_upload(uploaded_file, tipo)
    if not isinstance(texto, str):
        st.error("❌ Erro na extração de texto (retorno inválido).")
        return {}

    texto = texto.strip()
    if len(texto) < 20:
        st.error("⚠️ O documento não contém texto suficiente.")
        return {}

    # =======================
    # Payload MODERNO 2025-D4
    # =======================
    payload = {
        "artefato": artefato,
        "arquivo_original": nome,
        "tipo": tipo,
        "conteudo_textual": texto,
        "data_processamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origem": "insumos_v2025",
        "status": "ok",
    }

    # =======================
    # Persistência
    # =======================
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    arq_ultimo = os.path.join(base, f"{artefato}_ultimo.json")
    arq_ts = os.path.join(base, f"{artefato}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq_ts, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.success(f"✅ Insumo salvo e disponibilizado para o módulo **{artefato}**.")
        return payload

    except Exception as e:
        st.error(f"❌ Erro ao salvar JSON de insumo: {e}")
        return {}
