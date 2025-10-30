import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.ui_style import aplicar_estilo_global  # Mantém compatibilidade com SAAB 5.0

# ==========================
# Configuração da Página
# ==========================
st.set_page_config(page_title="⚠️ Alertas – SynapseNext", layout="wide", page_icon="⚠️")
aplicar_estilo_global()

# ==========================
# Cabeçalho
# ==========================
st.title("⚠️ Alertas")
st.markdown("### Monitoramento de Riscos e Anomalias do Ecossistema SAAB 5.0")
st.markdown("<hr>", unsafe_allow_html=True)

# ==========================
# Dados de Exemplo
# ==========================
dados_alertas = pd.DataFrame({
    "Categoria": ["Contratos", "DFDs", "ETPs", "TRs", "Editais"],
    "Quantidade": [4, 2, 3, 5, 1]
})

# ==========================
# Gráfico Responsivo
# ==========================
fig, ax = plt.subplots(figsize=(5.5, 2.8))  # proporções ajustadas para não ocupar toda a largura
bars = ax.bar(
    dados_alertas["Categoria"],
    dados_alertas["Quantidade"],
    color=["#D32F2F", "#FBC02D", "#388E3C", "#1976D2", "#7B1FA2"],
    edgecolor="black",
    linewidth=0.6
)

# Título e estilo do gráfico
ax.set_title("Distribuição de Alertas por Categoria", fontsize=11, fontweight="bold", pad=10)
ax.set_xlabel("Categoria", fontsize=9)
ax.set_ylabel("Quantidade", fontsize=9)
ax.tick_params(axis='x', labelrotation=15)
ax.grid(axis='y', linestyle="--", alpha=0.3)

# Margens e layout
plt.tight_layout(pad=1.5)

# Renderização no Streamlit (com largura adaptável)
st.pyplot(fig, use_container_width=True)

# ==========================
# Tabela de Detalhamento
# ==========================
st.markdown("#### 🧾 Detalhamento dos Alertas")
st.dataframe(dados_alertas, use_container_width=True)

# ==========================
# Rodapé Informativo
# ==========================
st.info("💡 Painel de alertas gerados automaticamente pelos validadores de integridade e consistência.")
st.markdown(
    "<br><small>© SynapseNext SAAB 5.0 – Núcleo de Inteligência Administrativa</small>",
    unsafe_allow_html=True
)
