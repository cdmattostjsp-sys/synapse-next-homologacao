# ==========================================================
# 📂 integration_insumos.py – Roteador Semântico de Insumos
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
#
# Este módulo centraliza o processamento dos insumos enviados
# pela página "Insumos", permitindo que o usuário selecione
# o artefato de destino (DFD, ETP, TR, EDITAL, CONTRATO etc.).
#
# Cada artefato é processado pela respectiva função dedicada:
#   - DFD     → utils/integration_dfd.processar_insumo()
#   - ETP     → utils/integration_etp.processar_insumo_etp()
#   - TR      → utils/integration_tr.processar_insumo_tr()
#   - EDITAL  → utils/integration_edital.processar_insumo_edital()
#
# O resultado é armazenado em st.session_state["insumo_processado"]
# e também em chaves específicas (dfd_campos_ai, etp_campos_ai etc.),
# para ser utilizado no preenchimento automático do artefato destino.
# ==========================================================

import streamlit as st

# Importações diretas dos processadores
from utils.integration_dfd import processar_insumo as processar_insumo_dfd
from utils.integration_etp import processar_insumo_etp
from utils.integration_tr import processar_insumo_tr

# Importação condicional (para evitar falhas em ambientes sem Edital)
try:
    from utils.integration_edital import processar_insumo_edital, integrar_com_contexto
except ModuleNotFoundError:
    processar_insumo_edital = None
    integrar_com_contexto = None


def processar_insumo_dinamico(arquivo, artefato: str) -> dict:
    """
    Encaminha o processamento do insumo para o módulo correto,
    permitindo início da jornada em qualquer etapa (DFD, ETP, TR, EDITAL).
    """

    artefato = artefato.upper().strip()
    resultado = {}

    try:
        # ======================================================
        # 🔹 DFD
        # ======================================================
        if artefato == "DFD":
            resultado = processar_insumo_dfd(arquivo, artefato)
            if "campos_ai" in resultado:
                st.session_state["dfd_campos_ai"] = resultado["campos_ai"]

        # ======================================================
        # 🔹 ETP
        # ======================================================
        elif artefato == "ETP":
            resultado = processar_insumo_etp(arquivo, artefato)
            if "campos_ai" in resultado:
                st.session_state["etp_campos_ai"] = resultado["campos_ai"]

        # ======================================================
        # 🔹 TR
        # ======================================================
        elif artefato == "TR":
            resultado = processar_insumo_tr(arquivo, artefato)
            if "campos_ai" in resultado:
                st.session_state["tr_campos_ai"] = resultado["campos_ai"]

        # ======================================================
        # 🔹 EDITAL
        # ======================================================
        elif artefato == "EDITAL":
            if processar_insumo_edital:
                contexto = integrar_com_contexto(st.session_state) if integrar_com_contexto else {}
                resultado = processar_insumo_edital(arquivo, contexto_previo=contexto)
                if "campos_ai" in resultado:
                    st.session_state["edital_campos_ai"] = resultado["campos_ai"]
            else:
                resultado = {"erro": "O módulo integration_edital.py ainda não está configurado."}

        # ======================================================
        # 🔹 CONTRATO (reserva futura)
        # ======================================================
        elif artefato == "CONTRATO":
            resultado = {"erro": "O módulo CONTRATO ainda não foi implementado."}

        else:
            resultado = {"erro": f"Artefato não reconhecido: {artefato}. Use DFD, ETP, TR ou EDITAL."}

    except Exception as e:
        resultado = {"erro": f"Falha no processamento do artefato {artefato}: {e}"}

    # ==========================================================
    # 🧾 Armazena o resultado no estado da sessão Streamlit
    # ==========================================================
    st.session_state["insumo_processado"] = resultado

    # ==========================================================
    # 🧠 Log leve para depuração
    # ==========================================================
    if "erro" not in resultado:
        print(
            f"[INSUMO] Artefato: {artefato} | "
            f"Arquivo: {getattr(arquivo, 'name', 'desconhecido')} | "
            f"Status: {resultado.get('status', 'indefinido')}"
        )
    else:
        print(f"[INSUMO] Erro ao processar {artefato}: {resultado['erro']}")

    return resultado
