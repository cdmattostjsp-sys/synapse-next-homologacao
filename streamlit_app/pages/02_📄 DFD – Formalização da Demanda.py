import streamlit as st
import json

st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide")
st.title("📄 DFD – Documento de Formalização da Demanda")
st.caption("Pré-preenchimento automático a partir de insumos + validação IA")

# ==========================================================
# 🔗 Verifica insumo ativo
# ==========================================================
if "last_insumo" not in st.session_state:
    st.warning("Nenhum insumo ativo encontrado. Envie um documento na aba 'Insumos' antes de continuar.")
else:
    insumo = st.session_state["last_insumo"]
    st.success(f"📎 Insumo ativo detectado: {insumo['nome']} (Artefato: {insumo['artefato']})")

    with st.expander("Prévia do insumo (texto legível)"):
        st.text(insumo["conteudo"][:2000])

    campos = insumo.get("campos_ai", {})

    # ==========================================================
    # 🧩 Formulário DFD com preenchimento automático
    # ==========================================================
    st.header("1️⃣ Entrada – Formulário institucional")

    unidade = st.text_input("Unidade solicitante", value=campos.get("unidade", ""))
    responsavel = st.text_input("Responsável pela demanda", value=campos.get("responsavel", ""))
    objeto = st.text_area("Objeto da contratação", value=campos.get("objeto", ""), height=150)
    justificativa = st.text_area("Justificativa da necessidade", value=campos.get("justificativa", ""), height=150)
    quantidade = st.text_area("Quantidade e escopo", value=campos.get("quantidade", ""), height=120)
    urgencia = st.text_area("Urgência ou prazo crítico", value=campos.get("urgencia", ""), height=100)
    riscos = st.text_area("Riscos e impactos da não contratação", value=campos.get("riscos", ""), height=100)
    alinhamento = st.text_area("Alinhamento com objetivos institucionais", value=campos.get("alinhamento", ""), height=100)

    if st.button("💾 Gerar rascunho de DFD"):
        dados_dfd = {
            "unidade": unidade,
            "responsavel": responsavel,
            "objeto": objeto,
            "justificativa": justificativa,
            "quantidade": quantidade,
            "urgencia": urgencia,
            "riscos": riscos,
            "alinhamento": alinhamento,
        }
        st.session_state["dfd_rascunho"] = dados_dfd
        st.success("Rascunho de DFD gerado com sucesso!")

        with st.expander("📋 Prévia JSON do DFD"):
            st.json(dados_dfd)
