# -*- coding: utf-8 -*-
# ==========================================================
# utils/integration_dfd.py
# SynapseNext – Integração com motor IA institucional v3
# ==========================================================

from __future__ import annotations
import json
import os
import re
from typing import Dict, Any
from pathlib import Path
import streamlit as st

# ==========================================================
# 📁 Diretórios e utilitários JSON
# ==========================================================
EXPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
DFD_JSON_PATH = os.path.join(EXPORTS_DIR, "dfd_data.json")

def ensure_exports_dir(path: str = EXPORTS_DIR) -> None:
    """Garante que o diretório de exportação exista."""
    os.makedirs(path, exist_ok=True)

def export_dfd_to_json(data: Dict[str, Any], path: str = DFD_JSON_PATH) -> str:
    """Salva metadados do DFD (dict) em JSON UTF-8. Retorna o caminho salvo."""
    ensure_exports_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path

def load_dfd_from_json(path: str = DFD_JSON_PATH) -> Dict[str, Any]:
    """Lê o arquivo JSON se existir; caso contrário, retorna {}."""
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

# ==========================================================
# 🧠 Integração com motor IA institucional v3
# ==========================================================
from utils.integration_ai_engine import processar_insumo as processar_insumo_ia

def obter_dfd_da_sessao() -> Dict[str, Any]:
    """
    Recupera dados de DFD processados via IA (st.session_state).
    Se não houver, tenta carregar do arquivo JSON exportado.
    """
    if "dfd_campos_ai" in st.session_state and st.session_state["dfd_campos_ai"]:
        return st.session_state["dfd_campos_ai"]
    if "last_insumo_dfd" in st.session_state:
        dados = st.session_state["last_insumo_dfd"]
        return dados.get("campos_ai", {})
    return load_dfd_from_json()

# ==========================================================
# 🤖 Processamento clássico (fallback)
# ==========================================================
def processar_insumo(arquivo, artefato: str = "DFD") -> dict:
    """
    Extrai texto e realiza inferência institucional usando o motor v3.
    Mantém compatibilidade com o pipeline clássico.
    """
    try:
        resultado = processar_insumo_ia(
            uploaded_file=arquivo,
            tipo_artefato=artefato,
            metadados_form={"origem": "integration_dfd.py"},
            filename=getattr(arquivo, "name", None)
        )
        campos = resultado.get("campos", {})
        st.session_state["dfd_campos_ai"] = campos
        export_dfd_to_json(campos)
        return {
            "artefato": artefato,
            "status": "processado",
            "campos_ai": campos
        }
    except Exception as e:
        return {"erro": f"Falha no motor institucional IA v3: {e}"}

# ==========================================================
# 🧩 Função pública principal
# ==========================================================
def carregar_dfd_para_formulario() -> Dict[str, Any]:
    """
    Retorna o dicionário de campos para pré-preenchimento do formulário DFD.
    Usa primeiro os dados da sessão ativa, depois fallback para arquivo.
    """
    dados = obter_dfd_da_sessao()
    if not dados:
        st.info("🔍 Nenhum DFD ativo na sessão. Utilize a aba Insumos para processar um documento.")
        return {}

    st.success("📎 Dados recebidos automaticamente do módulo INSUMOS (via sessão ativa).")
    return dados
