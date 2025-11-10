# ==========================================================
# utils/integration_dfd.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Módulo de integração entre o processamento de INSUMOS e o formulário DFD.
# Recupera automaticamente dados da sessão ativa ou do último JSON salvo.
# Compatível com motor IA institucional v3.
# Revisão: 2025-11-10
# ==========================================================

from __future__ import annotations
import os
import json
import glob
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

    # 1️⃣ Sessão ativa
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]

    base_dir = os.path.join("exports", "insumos", "json")
    ultimo_json = os.path.join(base_dir, "DFD_ultimo.json")

    # 2️⃣ Tenta carregar o último JSON persistido
    if os.path.exists(ultimo_json):
        campos = _carregar_dfd_de_arquivo(ultimo_json)
        if campos:
            st.session_state["dfd_campos_ai"] = campos
            return campos

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
            campos = _carregar_dfd_de_arquivo(arquivo)
            if campos:
                st.session_state["dfd_campos_ai"] = campos
                return campos
    except Exception as e:
        st.warning(f"⚠️ Nenhum DFD válido encontrado ({e})")

    # 4️⃣ Fallback seguro
    return {}


# ==========================================================
# 📥 Função auxiliar – carregar e limpar JSON
# ==========================================================
def _carregar_dfd_de_arquivo(caminho: str) -> dict:
    """Lê o arquivo JSON e interpreta o conteúdo IA (com limpeza de markdown)."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Prioriza o conteúdo vindo da IA institucional
        conteudo = None
        if "resultado_ia" in dados:
            # Pode ser dict direto ou string markdown
            resultado = dados["resultado_ia"]
            if isinstance(resultado, dict) and "resposta_texto" in resultado:
                conteudo = resultado["resposta_texto"]
            elif isinstance(resultado, str):
                conteudo = resultado
        elif "campos_ai" in dados:
            return dados["campos_ai"]
        elif "campos" in dados:
            return dados["campos"]

        if not conteudo:
            return {}

        # Limpeza de delimitadores markdown
        if isinstance(conteudo, str):
            conteudo = conteudo.strip()
            if conteudo.startswith("```json"):
                conteudo = conteudo.replace("```json", "").replace("```", "").strip()

            # Tenta decodificar o JSON interno
            try:
                parsed = json.loads(conteudo)
                if "DFD" in parsed:
                    parsed = parsed["DFD"]
                return parsed.get("secoes", parsed)
            except Exception:
                # Se não for JSON válido, devolve texto bruto
                return {"Conteúdo": conteudo}

        return conteudo

    except Exception as e:
        st.warning(f"⚠️ Falha ao ler {os.path.basename(caminho)}: {e}")
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
def status_dfd() -> str:
    """Retorna uma string de status para exibição no topo do módulo DFD."""
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return "✅ Dados carregados automaticamente (sessão ativa ou JSON)"
    base_dir = os.path.join("exports", "insumos", "json")
    if os.path.exists(os.path.join(base_dir, "DFD_ultimo.json")):
        return "🗂️ Dados disponíveis no último processamento de INSUMOS."
    return "⚠️ Nenhum DFD ativo encontrado – envie um insumo em '🔧 Insumos'."
