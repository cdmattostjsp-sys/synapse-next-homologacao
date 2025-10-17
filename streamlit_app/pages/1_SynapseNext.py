import streamlit as st
from utils.formatter_docx import markdown_to_docx
from utils.recommender_engine import generate_recommendations

# ============================
# CONFIGURAÇÃO GERAL
# ============================

st.set_page_config(
    page_title="SynapseNext – Ecossistema SAAB 5.0",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🧠 SynapseNext – Ecossistema SAAB 5.0")
st.caption("Ambiente integrado de apoio à fase interna das contratações públicas • SAAB/TJSP")

st.divider()

# ============================
# ESTRUTURA DE ABAS PRINCIPAIS
# ============================

tabs = st.tabs([
    "📘 DFD – Formalização da Demanda",
    "🧩 ETP – Estudo Técnico Preliminar",
    "📑 TR – Termo de Referência",
    "📜 Contrato",
    "🔍 Fiscalização"
])

# ============================
# ABA 1 – DFD
# ============================

with tabs[0]:
    st.header("📘 Documento de Formalização da Demanda (DFD)")
    st.markdown("Preencha as informações abaixo para gerar o rascunho do DFD institucional.")

    unidade = st.text_input("Unidade solicitante:")
    responsavel = st.text_input("Responsável (nome/cargo):")
    objeto = st.text_area("Objeto da contratação:")
    justificativa = st.text_area("Justificativa da necessidade:")
    quantidade = st.text_input("Quantidade / Dimensão do serviço:")
    urgencia = st.text_area("Urgência ou prazo limite:")
    riscos = st.text_area("Riscos identificados caso o pedido não seja atendido:")
    alinhamento = st.text_input("Alinhamento institucional:")
    suporte = st.text_input("Documentos de suporte (opcional):")

    st.divider()
    if st.button("Gerar Rascunho DFD"):
        texto = f"""
        **Documento de Formalização da Demanda (DFD)**  
        Unidade Solicitante: {unidade}  
        Responsável: {responsavel}  

        **1️⃣ Descrição do Objeto**  
        {objeto}

        **2️⃣ Justificativa da Necessidade**  
        {justificativa}

        **3️⃣ Quantidade, Urgência e Riscos**  
        {quantidade}  
        {urgencia}  
        {riscos}

        **4️⃣ Alinhamento Institucional**  
        {alinhamento}

        **5️⃣ Documentos de Suporte**  
        {suporte}
        """
        st.markdown(texto)
        st.success("✅ Rascunho do DFD gerado com sucesso!")
        st.download_button("⬇️ Baixar Rascunho em DOCX", texto, file_name="DFD_SynapseNext.docx")

# ============================
# ABA 2 – ETP
# ============================

with tabs[1]:
    st.header("🧩 Estudo Técnico Preliminar (ETP)")
    st.markdown("Estrutura base para elaboração do ETP. Campos e recomendações virão das próximas integrações.")

    st.info("💡 Esta aba será expandida com a análise comparativa de soluções e critérios técnicos de seleção.")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Problema a ser resolvido:")
        st.text_area("Alternativas consideradas:")
    with col2:
        st.text_area("Critérios de escolha da solução:")
        st.text_area("Impactos esperados:")

    if st.button("Gerar Rascunho ETP"):
        st.success("🧩 Modelo inicial do ETP gerado (placeholder para próxima etapa).")

# ============================
# ABA 3 – TR
# ============================

with tabs[2]:
    st.header("📑 Termo de Referência (TR)")
    st.markdown("Base estrutural para desenvolvimento do Termo de Referência.")

    st.info("💡 Nesta aba serão incluídos campos automáticos de especificação técnica, estimativa de custos e matriz de riscos.")
    st.text_area("Especificações técnicas:")
    st.text_area("Estimativa de custos:")
    st.text_area("Critérios de julgamento:")

    if st.button("Gerar Rascunho TR"):
        st.success("📑 Estrutura do TR gerada (em construção).")

# ============================
# ABA 4 – CONTRATO
# ============================

with tabs[3]:
    st.header("📜 Minuta de Contrato")
    st.markdown("Modelo básico da minuta contratual a ser aprimorada com variáveis e cláusulas padrão.")

    st.info("💡 Este módulo futuramente permitirá selecionar modelos por tipo de contrato (obra, serviço, fornecimento etc.)")
    tipo_contrato = st.selectbox("Tipo de contrato:", ["Serviço", "Obra", "Fornecimento", "Outro"])
    prazo = st.text_input("Prazo de execução:")
    clausulas = st.text_area("Cláusulas específicas:")

    if st.button("Gerar Rascunho de Contrato"):
        st.success(f"📜 Rascunho de contrato do tipo {tipo_contrato} gerado com sucesso!")

# ============================
# ABA 5 – FISCALIZAÇÃO
# ============================

with tabs[4]:
    st.header("🔍 Fiscalização Contratual")
    st.markdown("Módulo para registro e acompanhamento de execuções contratuais.")

    st.info("💡 Este módulo incluirá dashboards de acompanhamento e alertas de vencimentos de prazos.")
    st.text_input("Número do contrato:")
    st.text_area("Resumo da execução:")
    st.text_area("Ocorrências registradas:")
    st.text_area("Penalidades ou recomendações:")

    if st.button("Gerar Relatório de Fiscalização"):
        st.success("🔍 Relatório de fiscalização gerado (placeholder para futura integração).")

st.divider()
st.caption("SynapseNext • SAAB/TJSP – Protótipo v1.0 (Abas Integradas)")
