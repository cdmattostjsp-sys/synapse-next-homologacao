# ==========================================================
# 📂 integration_insumos.py – Roteador Semântico de Insumos
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
#
# Este módulo centraliza o processamento dos insumos enviados
# pela página "Insumos", permitindo que o usuário selecione
# o artefato de destino (DFD, ETP, TR etc.).
#
# Cada artefato é processado pela respectiva função dedicada:
#   - DFD → utils/integration_dfd.processar_insumo()
#   - ETP → utils/integration_etp.processar_insumo_etp()
#   - TR  → utils/integration_tr.processar_insumo_tr()
#
# O resultado é armazenado em st.session_state["insumo_processado"]
# para ser utilizado pelo módulo de destino no preenchimento do
# formulário e posterior geração do artefato institucional.
# ==========================================================

import streamlit as st

# Importa os processadores específicos de cada módulo
from utils.integration_dfd import processar_insumo as processar_insumo_dfd
from utils.integration_etp import processar_insumo_etp
from utils.integration_tr import processar_insumo_tr


def processar_insumo_dinamico(arquivo, artefato: str) -> dict:
    """
    Encaminha o processamento do insumo para o módulo correto,
    permitindo início da jornada em qualquer etapa (DFD, ETP, TR).
    """

    artefato = artefato.upper().strip()
    resultado = {}

    try:
        if artefato == "DFD":
            resultado = processar_insumo_dfd(arquivo, artefato)
        elif artefato == "ETP":
            resultado = processar_insumo_etp(arquivo, artefato)
        elif artefato == "TR":
            resultado = processar_insumo_tr(arquivo, artefato)
        else:
            resultado = {
                "erro": f"Artefato não reconhecido: {artefato}. "
                        "Use DFD, ETP ou TR."
            }
    except Exception as e:
        resultado = {"erro": f"Falha no processamento: {e}"}

    # Guarda o resultado no estado da sessão Streamlit
    st.session_state["insumo_processado"] = resultado

    # Log leve no console para depuração (Codespaces/Streamlit)
    if "erro" not in resultado:
        print(
            f"[INSUMO] Artefato: {artefato} | "
            f"Arquivo: {getattr(arquivo, 'name', 'desconhecido')} | "
            f"Status: {resultado.get('status', 'indefinido')}"
        )
    else:
        print(f"[INSUMO] Erro ao processar {artefato}: {resultado['erro']}")

    return resultado
