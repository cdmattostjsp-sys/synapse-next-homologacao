# ==========================================================
# 📂 integration_insumos.py – Roteador Semântico de Insumos
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
#
# Centraliza o processamento dos insumos enviados pela página "Insumos",
# permitindo que o usuário selecione o artefato de destino (DFD, ETP, TR,
# EDITAL ou CONTRATO).
#
# Cada artefato é processado pela respectiva função dedicada:
#   - DFD     → utils/integration_dfd.processar_insumo()
#   - ETP     → utils/integration_etp.processar_insumo_etp()
#   - TR      → utils/integration_tr.processar_insumo_tr()
#   - EDITAL  → utils/integration_edital.processar_insumo_edital()
#   - CONTRATO→ utils/integration_contrato.processar_insumo_contrato()
#
# O resultado é armazenado em st.session_state["insumo_processado"]
# e também em chaves específicas (dfd_campos_ai, etp_campos_ai etc.),
# para preenchimento automático do artefato de destino.
# ==========================================================

import streamlit as st

# ==========================================================
# 🔗 Importações diretas dos módulos existentes
# ==========================================================
from utils.integration_dfd import processar_insumo as processar_insumo_dfd
from utils.integration_etp import processar_insumo_etp
from utils.integration_tr import processar_insumo_tr

# ==========================================================
# 🔄 Importações condicionais (Edital e Contrato)
# ==========================================================
try:
    from utils.integration_edital import processar_insumo_edital, integrar_com_contexto as integrar_contexto_edital
except ModuleNotFoundError:
    processar_insumo_edital = None
    integrar_contexto_edital = None

try:
    from utils.integration_contrato import processar_insumo_contrato, integrar_com_contexto as integrar_contexto_contrato
except ModuleNotFoundError:
    processar_insumo_contrato = None
    integrar_contexto_contrato = None


# ==========================================================
# ⚙️ Função principal
# ==========================================================
def processar_insumo_dinamico(arquivo, artefato: str) -> dict:
    """
    Encaminha o processamento do insumo para o módulo correto.
    Permite início da jornada em qualquer etapa (DFD, ETP, TR, EDITAL, CONTRATO).
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
                contexto = integrar_contexto_edital(st.session_state) if integrar_contexto_edital else {}
                resultado = processar_insumo_edital(arquivo, contexto_previo=contexto)
                if "campos_ai" in resultado:
                    st.session_state["edital_campos_ai"] = resultado["campos_ai"]
            else:
                resultado = {"erro": "O módulo integration_edital.py ainda não está configurado."}

        # ======================================================
        # 🔹 CONTRATO
        # ======================================================
        elif artefato == "CONTRATO":
            if processar_insumo_contrato:
                contexto = integrar_contexto_contrato(st.session_state) if integrar_contexto_contrato else {}
                resultado = processar_insumo_contrato(arquivo, artefato, contexto_previo=contexto)
                if "campos_ai" in resultado:
                    st.session_state["contrato_campos_ai"] = resultado["campos_ai"]
            else:
                resultado = {"erro": "O módulo integration_contrato.py ainda não está configurado."}

        # ======================================================
        # ❌ Artefato desconhecido
        # ======================================================
        else:
            resultado = {"erro": f"Artefato não reconhecido: {artefato}. Use DFD, ETP, TR, EDITAL ou CONTRATO."}

    except Exception as e:
        resultado = {"erro": f"Falha no processamento do artefato {artefato}: {e}"}

    # ==========================================================
    # 🧾 Registro no estado da sessão
    # ==========================================================
    st.session_state["insumo_processado"] = resultado

    # ==========================================================
    # 🧠 Log leve para depuração (Streamlit Cloud)
    # ==========================================================
    if "erro" not in resultado:
        print(
            f"[INSUMO] Artefato: {artefato} | "
            f"Arquivo: {getattr(arquivo, 'name', 'desconhecido')} | "
            f"Status: {resultado.get('status', 'indefinido')}"
        )
    else:
        print(f"[INSUMO] ❌ Erro ao processar {artefato}: {resultado['erro']}")

    return resultado
