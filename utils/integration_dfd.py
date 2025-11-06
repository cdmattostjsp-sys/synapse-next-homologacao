# ==========================================================
# utils/integration_dfd.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão Engenheiro Synapse – vNext_2025.11.08 (corrigido)
# Compatibilidade: Streamlit 1.39.0 + openai 2.7.1
# ==========================================================

import json
from pathlib import Path
import streamlit as st

# ==========================================================
# 📁 Funções utilitárias de caminho
# ==========================================================
def get_possible_dfd_paths() -> list[Path]:
    """
    Retorna os possíveis caminhos onde o DFD_ultimo.json pode estar armazenado.
    Inclui tanto o modo persistente (exports) quanto o modo volátil (/tmp).
    """
    return [
        Path("exports/insumos/json/DFD_ultimo.json"),
        Path("/tmp/insumos/json/DFD_ultimo.json"),
    ]


# ==========================================================
# 🔍 Função principal: carregar o DFD da sessão
# ==========================================================
def obter_dfd_da_sessao():
    """
    Tenta carregar o último DFD gerado, seja em exports/insumos/json ou /tmp/insumos/json.
    Essa função permite que o app Streamlit funcione corretamente em ambientes
    com restrição de gravação (como Streamlit Cloud).
    """
    try:
        caminhos = get_possible_dfd_paths()

        for caminho in caminhos:
            if caminho.exists():
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                print(f"[SynapseNext][DFD] Dados importados de {caminho}")
                return dados

        print("[SynapseNext][DFD] Nenhum DFD encontrado em nenhum diretório padrão.")
        return None

    except Exception as e:
        print(f"[ERRO][DFD] Falha ao carregar DFD: {e}")
        return None


# ==========================================================
# 💾 Função auxiliar: salvar manualmente um DFD (opcional)
# ==========================================================
def salvar_dfd_manual(dados: dict, nome_arquivo: str = "DFD_manual.json"):
    """
    Salva manualmente um DFD para depuração ou teste.
    Tenta primeiro em exports/insumos/json, e recorre ao /tmp/insumos/json se necessário.
    """
    try:
        base_paths = [
            Path("exports/insumos/json"),
            Path("/tmp/insumos/json")
        ]

        for base_path in base_paths:
            try:
                base_path.mkdir(parents=True, exist_ok=True)
                destino = base_path / nome_arquivo
                with open(destino, "w", encoding="utf-8") as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                print(f"[SynapseNext][DFD] Arquivo salvo com sucesso em: {destino}")
                return destino
            except Exception:
                continue

        print("[ERRO][DFD] Nenhum diretório pôde ser usado para salvar o DFD.")
        return None

    except Exception as e:
        print(f"[ERRO][DFD] Falha ao salvar DFD manualmente: {e}")
        return None


# ==========================================================
# 🧠 Integração Streamlit (opcional)
# ==========================================================
def exibir_dfd_em_pagina():
    """
    Exibe o DFD carregado na interface Streamlit.
    Pode ser chamado diretamente na página do módulo DFD.
    """
    dados = obter_dfd_da_sessao()

    if not dados:
        st.warning("⚠️ Nenhum DFD encontrado. Gere um insumo primeiro na página 'Insumos'.")
        return

    st.success("✅ DFD carregado com sucesso!")
    st.json(dados)
