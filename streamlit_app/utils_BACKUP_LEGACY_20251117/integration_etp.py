# ==========================================================
# utils/integration_etp.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Integração entre o processamento de INSUMOS e o módulo ETP.
# Recupera automaticamente dados da sessão ativa ou do último JSON salvo.
# Compatível com o motor IA institucional v3 e persistência híbrida.
# ==========================================================

from __future__ import annotations
import os
import json
import glob
import streamlit as st
from datetime import datetime

# ==========================================================
# 🧠 Função principal – obter ETP ativo
# ==========================================================
def obter_etp_da_sessao() -> dict:
    """
    Recupera o dicionário de campos do ETP ativo.

    Prioridades:
    1️⃣ st.session_state["etp_campos_ai"]
    2️⃣ exports/insumos/json/ETP_ultimo.json
    3️⃣ Último arquivo ETP_*.json no diretório de insumos
    """

    # 1️⃣ Sessão ativa
    if "etp_campos_ai" in st.session_state and st.session_state["etp_campos_ai"]:
        return st.session_state["etp_campos_ai"]

    # 2️⃣ Último insumo salvo (ETP_ultimo.json)
    base_dir = os.path.join("exports", "insumos", "json")
    ultimo_json = os.path.join(base_dir, "ETP_ultimo.json")

    if os.path.exists(ultimo_json):
        try:
            with open(ultimo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
            campos = dados.get("campos_ai", {}) or dados.get("campos", {})
            if campos:
                st.session_state["etp_campos_ai"] = campos
                return campos
        except Exception as e:
            st.warning(f"⚠️ Falha ao ler ETP_ultimo.json: {e}")

    # 3️⃣ Busca o arquivo mais recente (fallback final)
    try:
        arquivos = sorted(
            glob.glob(os.path.join(base_dir, "ETP_*.json")),
            key=os.path.getmtime,
            reverse=True,
        )
        for arquivo in arquivos:
            if "ETP_ultimo.json" in arquivo:
                continue
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            campos = dados.get("campos_ai", {}) or dados.get("campos", {})
            if campos:
                st.session_state["etp_campos_ai"] = campos
                return campos
    except Exception as e:
        st.warning(f"⚠️ Nenhum ETP válido encontrado ({e})")

    # 4️⃣ Fallback seguro
    return {}


# ==========================================================
# 💾 Função auxiliar – salvar ETP gerado pelo formulário
# ==========================================================
def salvar_etp_em_json(campos_etp: dict, origem: str = "formulario") -> str:
    """
    Salva o conteúdo atual do formulário ETP em /exports/insumos/json.
    Utilizado tanto para IA quanto para preenchimento manual.
    """
    base_dir = os.path.join("exports", "insumos", "json")
    os.makedirs(base_dir, exist_ok=True)

    payload = {
        "artefato": "ETP",
        "origem": origem,
        "campos_ai": campos_etp,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arquivo_ultimo = os.path.join(base_dir, "ETP_ultimo.json")
    arquivo_timestamp = os.path.join(base_dir, f"ETP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        with open(arquivo_timestamp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        st.session_state["etp_campos_ai"] = campos_etp
        return arquivo_ultimo
    except Exception as e:
        st.warning(f"⚠️ Falha ao salvar ETP: {e}")
        return ""


# ==========================================================
# 🧩 Função utilitária – status legível
# ==========================================================
def status_etp():
    """Retorna uma string de status para exibição no topo do módulo ETP."""
    if "etp_campos_ai" in st.session_state and st.session_state["etp_campos_ai"]:
        return "✅ Dados carregados automaticamente (sessão ativa ou JSON)"
    base_dir = os.path.join("exports", "insumos", "json")
    if os.path.exists(os.path.join(base_dir, "ETP_ultimo.json")):
        return "🗂️ Dados disponíveis no último processamento de INSUMOS."
    return "⚠️ Nenhum ETP ativo encontrado – envie um insumo em '🔧 Insumos'."
