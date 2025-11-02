# ==========================================================
# pages/02_📄 DFD – Formalização da Demanda.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Documento de Formalização da Demanda (DFD)
# Pré-preenchimento automático via módulo INSUMOS + IA Institucional v3
# ==========================================================

import streamlit as st
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.integration_dfd import carregar_dfd_para_formulario, export_dfd_to_json

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide", page_icon="📄")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📄 Documento de Formalização da Demanda (DFD)",
    "Pré-preenchimento automático a partir de insumos e validação IA institucional."
)
st.divider()

# ==========================================================
# 📦 Carregamento automático de dados do módulo INSUMOS
# ==========================================================
dados_ai = carregar_dfd_para_formulario()

if dados_ai:
    st.success("📎 Dados recebidos automaticamente do módulo INSUMOS (via sessão ativa).")
else:
    st.info("Envie um documento na aba 🔧 **Insumos** para gerar o pré-preenchimento automático.")

st.divider()

# ==========================================================
# 🧾 Entrada – Formulário Institucional
# ==========================================================
st.subheader("🧾 1. Entrada – Formulário Institucional")

col1, col2 = st.columns(2)
with col1:
    unidade = st.text_input(
        "Unidade solicitante",
        value=dados_ai.get("unidade_solicitante", "")
    )
with col2:
    responsavel = st.text_input(
        "Responsável pela demanda",
        value=dados_ai.get("responsavel", dados_ai.get("responsavel_tecnico", ""))
    )

objeto = st.text_area("Objeto da contratação", value=dados_ai.get("objeto", ""), height=100)
justificativa = st.text_area("Justificativa técnica", value=dados_ai.get("justificativa", ""), height=100)

col3, col4 = st.columns(2)
with col3:
    quantidade = st.text_input("Quantidade estimada", value=dados_ai.get("quantidade", ""))
with col4:
    urgencia = st.selectbox(
        "Grau de urgência",
        ["Baixa", "Média", "Alta"],
        index=0 if not dados_ai.get("urgencia") else ["Baixa", "Média", "Alta"].index(
            dados_ai["urgencia"].capitalize()) if dados_ai["urgencia"].capitalize() in ["Baixa", "Média", "Alta"] else 0
    )

riscos = st.text_area("Riscos associados", value=dados_ai.get("riscos", ""), height=100)
alinhamento = st.text_area("Alinhamento com planejamento estratégico", value=dados_ai.get("alinhamento_planejamento", ""), height=100)

# ==========================================================
# 🧩 Montagem final do DFD
# ==========================================================
dfd_dados = {
    "unidade_solicitante": unidade,
    "responsavel": responsavel,
    "objeto": objeto,
    "justificativa": justificativa,
    "quantidade": quantidade,
    "urgencia": urgencia,
    "riscos": riscos,
    "alinhamento_planejamento": alinhamento,
}

# ==========================================================
# 💾 Botão de exportação e confirmação
# ==========================================================
st.divider()
if st.button("💾 Salvar e Exportar DFD"):
    path = export_dfd_to_json(dfd_dados)
    st.success(f"✅ DFD salvo com sucesso em: `{path}`")
    st.json(dfd_dados)
else:
    st.caption("Após revisar os campos, clique em **Salvar e Exportar DFD** para armazenar o documento.")

# ==========================================================
# 🏁 Rodapé institucional
# ==========================================================
st.divider()
st.caption("📄 Módulo DFD – SynapseNext (TJSP/SAAB). Integração ativa com IA Institucional v3.")
