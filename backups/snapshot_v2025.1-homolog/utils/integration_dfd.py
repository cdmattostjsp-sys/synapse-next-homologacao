# ======================================================================
# utils/integration_dfd.py — VERSÃO FINAL 2025-D9 (ESTÁVEL)
# Compatível com DocumentAgent(D3) + IAClient vNext
# Fluxo: INSUMOS → DFD → IA → Formulário Moderno → Exportação
# ======================================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime


# ======================================================================
# 🔧 Remover blocos Markdown/formatadores
# ======================================================================
def _limpar_markdown(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    return (
        texto.replace("```json", "")
        .replace("```", "")
        .replace("“", '"')
        .replace("”", '"')
        .strip()
    )


# ======================================================================
# 📥 Leitura de arquivos DFD/insumo
# ======================================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return {}

    # Caso 1 — DFD consolidado (formulário)
    if isinstance(dados.get("campos_ai"), dict):
        return dados["campos_ai"]

    # Caso 2 — IA moderna
    if isinstance(dados.get("resultado_ia"), dict):
        bruto = dados["resultado_ia"]
        if "DFD" in bruto and isinstance(bruto["DFD"], dict):
            return bruto["DFD"]
        return bruto

    # Caso 3 — insumo bruto
    texto = dados.get("conteudo_textual")
    if isinstance(texto, str) and len(texto.strip()) > 20:
        return {
            "unidade_demandante": "",
            "responsavel": "",
            "prazo_estimado": "",
            "valor_estimado": "0,00",
            "descricao_necessidade": texto.strip(),
            "motivacao": "",
            "texto_narrativo": texto.strip(),
            "secoes": {},
            "lacunas": [],
        }

    return {}


# ======================================================================
# 🔄 Obter DFD: sessão → último arquivo → histórico
# ======================================================================
def obter_dfd_da_sessao() -> dict:

    if "dfd_campos_ai" in st.session_state:
        if isinstance(st.session_state["dfd_campos_ai"], dict):
            if st.session_state["dfd_campos_ai"]:
                return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    arquivos = sorted(
        glob.glob(os.path.join(base, "DFD_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )

    for arq in arquivos:
        if arq.endswith("DFD_ultimo.json"):
            continue
        dados = _carregar_dfd_de_arquivo(arq)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    return {}


# ======================================================================
# 💾 Salvar DFD consolidado
# ======================================================================
def salvar_dfd_em_json(campos: dict, origem: str = "dfd_moderno_streamlit") -> str:

    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": campos,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arq1 = os.path.join(base, "DFD_ultimo.json")
    arq2 = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq1, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq2, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.session_state["dfd_campos_ai"] = campos
        return arq1

    except Exception:
        return ""


# ======================================================================
# 🧠 IA → Gerar rascunho moderno (mantém JSON integral)
# ======================================================================
def gerar_rascunho_dfd_com_ia() -> dict:

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if not os.path.exists(ultimo):
        st.warning("Nenhum insumo encontrado.")
        return {}

    try:
        with open(ultimo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        texto = (dados.get("conteudo_textual") or "").strip()
    except Exception:
        st.error("Erro ao ler insumo.")
        return {}

    if len(texto) < 20:
        st.error("Texto insuficiente para IA.")
        return {}

    try:
        from agents.document_agent import processar_dfd_com_ia
        bruto = processar_dfd_com_ia(texto)

        if "resultado_ia" in bruto and isinstance(bruto["resultado_ia"], dict):
            bruto = bruto["resultado_ia"]

        if "DFD" in bruto and isinstance(bruto["DFD"], dict):
            bruto = bruto["DFD"]

        st.session_state["dfd_campos_ai"] = bruto
        return bruto

    except Exception as e:
        st.error(f"Erro IA: {e}")
        return {}


# ======================================================================
# 📌 Status rápido
# ======================================================================
def status_dfd() -> str:
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    if os.path.exists(ultimo):
        return "🗂️ DFD disponível nos insumos processados"

    return "⚠️ Nenhum DFD disponível — envie um insumo no módulo INSUMOS."
