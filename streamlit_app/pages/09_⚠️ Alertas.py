import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.ui_style import aplicar_estilo_global

st.set_page_config(page_title="⚠️ Alertas – SynapseNext", layout="wide", page_icon="⚠️")
aplicar_estilo_global()

st.title("⚠️ Alertas")
st.markdown("### Monitoramento de Riscos e Anomalias do Ecossistema SAAB 5.0")
st.markdown("<hr>", unsafe_allow_html=True)

dados_alertas = pd.DataFrame({
    "Categoria": ["Contratos", "DFDs", "ETPs", "TRs", "Editais"],
    "Quantidade": [4, 2, 3, 5, 1]
})

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(dados_alertas["Categoria"], dados_alertas["Quantidade"],
       color=["#D32F2F", "#FBC02D", "#388E3C", "#1976D2", "#7B1FA2"])
ax.set_title("Distribuição de Alertas por Categoria", fontsize=11, fontweight="bold")
ax.set_ylabel("Quantidade", fontsize=9)
st.pyplot(fig)

st.markdown("#### Detalhamento dos Alertas")
st.dataframe(dados_alertas, use_container_width=True)
st.info("💡 Painel de alertas gerados automaticamente pelos validadores de integridade e consistência.")
st.markdown("<br><small>© SynapseNext SAAB 5.0 – Núcleo de Inteligência Administrativa</small>", unsafe_allow_html=True)
