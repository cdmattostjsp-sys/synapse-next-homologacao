# ==========================================================
# utils/integration_dfd.py – VERSÃO CORRETA E COMPLETA
# ==========================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime

# ----------------------------------------------------------
# 🔄 LIMPAR BLOCOS MARKDOWN ```json
# ----------------------------------------------------------
def _limpar_markdown(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    t = texto.strip()
    t = t.replace("```json", "").replace("```", "").strip()
    return t

# ----------------------------------------------------------
# 📥 CARREGAR JSON BRUTO DO ARQUIVO
# ----------------------------------------------------------
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # 1) Conteúdo vindo da IA
        if "resultado_ia" in dados:
            r = dados["resultado_ia"]
            if isinstance(r, dict) and "resposta_texto" in r:
                bruto = r["resposta_texto"]
            elif isinstance(r, str):
                bruto = r
            else:
                bruto = ""
        # 2) Campos diretos
        elif "campos_ai" in dados:
            return dados["campos_ai"]
        elif "campos" in dados:
            return dados["campos"]
        else:
            bruto = ""

        bruto = _limpar_markdown(bruto)

        try:
            parsed = json.loads(bruto)
            if "DFD" in parsed:
                return parsed["DFD"]
            return parsed
        except:
            return {"conteudo": bruto}

    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {os.path.basename(caminho)}: {e}")
        return {}

# ----------------------------------------------------------
# 🧠 OBTER O DFD ATIVO
# ----------------------------------------------------------
def obter_dfd_da_sessao() -> dict:

    # 1️⃣ Sessão ativa
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base = os.path.join("exports", "insumos", "json")
    ultimo = os.path.join(base, "DFD_ultimo.json")

    # 2️⃣ Carrega o último JSON salvo
    if os.path.exists(ultimo):
        dados = _carregar_dfd_de_arquivo(ultimo)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    # 3️⃣ Tenta encontrar outro JSON DFD_*.json
    arquivos = sorted(
        glob.glob(os.path.join(base, "DFD_*.json")),
        key=os.path.getmtime,
        reverse=True,
    )

    for arq in arquivos:
        if "DFD_ultimo" in arq:
            continue
        dados = _carregar_dfd_de_arquivo(arq)
        if dados:
            st.session_state["dfd_campos_ai"] = dados
            return dados

    return {}

# ----------------------------------------------------------
# 💾 SALVAR DFD
# ----------------------------------------------------------
def salvar_dfd_em_json(campos_dfd: dict, origem: str = "formulario") -> str:
    base = os.path.join("exports", "insumos", "json")
    os.makedirs(base, exist_ok=True)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": campos_dfd,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arq1 = os.path.join(base, "DFD_ultimo.json")
    arq2 = os.path.join(base, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arq1, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        with open(arq2, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        st.session_state["dfd_campos_ai"] = campos_dfd
        return arq1

    except Exception as e:
        st.error(f"❌ Falha ao salvar DFD: {e}")
        return ""

# ----------------------------------------------------------
# 🧩 STATUS DO DFD
# ----------------------------------------------------------
def status_dfd() -> str:
    """Mensagem amigável para exibir no topo do módulo."""
    base = os.path.join("exports", "insumos", "json")
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ DFD carregado automaticamente (sessão ativa)"
    if os.path.exists(os.path.join(base, "DFD_ultimo.json")):
        return "🗂️ DFD disponível a partir dos insumos processados"
    return "⚠️ Nenhum DFD disponível — envie um insumo pelo módulo INSUMOS"

