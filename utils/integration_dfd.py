# ==========================================================
# utils/integration_dfd.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão Engenheiro Synapse – vNext_2025.11.07
# ==========================================================
# Módulo de integração entre o processamento de INSUMOS e o formulário DFD.
# Recupera automaticamente dados da sessão ativa ou do último JSON salvo.
# Compatível com motor IA institucional v3.
# ==========================================================

from __future__ import annotations
import os
import json
import glob
import re
import streamlit as st
from datetime import datetime

# ==========================================================
# 🧠 Função principal – obter DFD ativo
# ==========================================================
def obter_dfd_da_sessao() -> dict:
    """
    Recupera o dicionário de campos do DFD ativo.

    Prioridades:
    1️⃣ st.session_state["dfd_campos_ai"]
    2️⃣ exports/insumos/json/DFD_ultimo.json
    3️⃣ Último arquivo DFD_*.json no diretório de insumos
    """

    # 1️⃣ Verifica sessão ativa
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    # 2️⃣ Tenta carregar o último insumo salvo (DFD_ultimo.json)
    base_dir = os.path.join("exports", "insumos", "json")
    ultimo_json = os.path.join(base_dir, "DFD_ultimo.json")

    if os.path.exists(ultimo_json):
        try:
            with open(ultimo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)

            # 🔹 Eng. Synapse – interpretar resposta da IA se presente
            campos = dados.get("campos_ai", {}) or dados.get("campos", {})
            if not campos and "resultado_ia" in dados:
                resposta = dados["resultado_ia"].get("resposta_texto", "")
                if resposta:
                    # Extrai conteúdo JSON de blocos markdown ```json ... ```
                    match = re.search(r"```json(.*?)```", resposta, re.S)
                    if match:
                        conteudo_json = match.group(1).strip()
                        try:
                            campos = json.loads(conteudo_json)
                        except json.JSONDecodeError:
                            st.warning("⚠️ A resposta da IA contém JSON parcial – tentando parsear texto bruto.")
                            try:
                                # tentativa de recuperação básica
                                conteudo_json = conteudo_json.strip("` \n\t")
                                campos = json.loads(conteudo_json)
                            except Exception:
                                campos = {}
            
            if campos:
                st.session_state["dfd_campos_ai"] = campos
                return campos

        except Exception as e:
            st.warning(f"⚠️ Falha ao ler DFD_ultimo.json: {e}")

    # 3️⃣ Busca o arquivo DFD mais recente (fallback final)
    try:
        arquivos = sorted(
            glob.glob(os.path.join(base_dir, "DFD_*.json")),
            key=os.path.getmtime,
            reverse=True,
        )
        for arquivo in arquivos:
            if "DFD_ultimo.json" in arquivo:
                continue
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            campos = dados.get("campos_ai", {}) or dados.get("campos", {})
            if campos:
                st.session_state["dfd_campos_ai"] = campos
                return campos
    except Exception as e:
        st.warning(f"⚠️ Nenhum DFD válido encontrado ({e})")

    # 4️⃣ Fallback seguro
    return {}


# ==========================================================
# 💾 Função auxiliar – salvar DFD gerado pelo formulário
# ==========================================================
def salvar_dfd_em_json(campos_dfd: dict, origem: str = "formulario") -> str:
    """
    Salva o conteúdo atual do formulário DFD em /exports/insumos/json.
    Utilizado tanto para IA quanto para preenchimento manual.
    """
    base_dir = os.path.join("exports", "insumos", "json")
    os.makedirs(base_dir, exist_ok=True)

    payload = {
        "artefato": "DFD",
        "origem": origem,
        "campos_ai": campos_dfd,
        "data_salvamento": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    arquivo_ultimo = os.path.join(base_dir, "DFD_ultimo.json")
    arquivo_timestamp = os.path.join(base_dir, f"DFD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(arquivo_ultimo, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        with open(arquivo_timestamp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        st.session_state["dfd_campos_ai"] = campos_dfd
        return arquivo_ultimo
    except Exception as e:
        st.warning(f"⚠️ Falha ao salvar DFD: {e}")
        return ""


# ==========================================================
# 🧩 Função utilitária – status legível
# ==========================================================
def status_dfd():
    """Retorna uma string de status para exibição no topo do módulo DFD."""
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ Dados carregados automaticamente (sessão ativa ou JSON)"
    base_dir = os.path.join("exports", "insumos", "json")
    if os.path.exists(os.path.join(base_dir, "DFD_ultimo.json")):
        return "🗂️ Dados disponíveis no último processamento de INSUMOS."
    return "⚠️ Nenhum DFD ativo encontrado – envie um insumo em '🔧 Insumos'."
