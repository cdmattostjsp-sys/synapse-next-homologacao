# ============================================
#  utils/layout_manager.py
#  SAAB 5.0 – Gerenciador de Layout e Gráficos
# ============================================
#
#  Objetivo:
#  Padronizar proporções, margens, títulos e legendas
#  de gráficos e containers em todo o ecossistema SynapseNext.
#  Mantém compatibilidade total com Plotly, Matplotlib e Streamlit.
#
#  Versão: 1.0 (2025-10-30)
#  Autor: Synapse.Engineer
#  Órgão: TJSP / SAAB
# ============================================

import streamlit as st
from plotly.graph_objs import Figure

# ---------------------------------------------------------
# Configurações padrão SAAB 5.0
# ---------------------------------------------------------
LAYOUT_CONFIG = {
    "altura_padrao": 450,
    "largura_padrao": 900,
    "margem": dict(l=40, r=40, t=60, b=40),
    "fonte_titulo": 18,
    "fonte_legenda": 12,
    "cor_primaria": "#004A8F",
    "cor_secundaria": "#007ACC",
    "fonte_base": "Inter",
}


# ---------------------------------------------------------
# 1️⃣ Função para aplicar layout padronizado a gráficos Plotly
# ---------------------------------------------------------
def ajustar_grafico(fig: Figure, titulo: str = None, altura=None, largura=None):
    """
    Aplica proporções e estilos padronizados SAAB 5.0 a um gráfico Plotly.

    :param fig: objeto plotly.graph_objs.Figure
    :param titulo: título opcional do gráfico
    :param altura: altura customizada (padrão: 450)
    :param largura: largura customizada (padrão: 900)
    :return: gráfico ajustado
    """
    altura = altura or LAYOUT_CONFIG["altura_padrao"]
    largura = largura or LAYOUT_CONFIG["largura_padrao"]

    fig.update_layout(
        height=altura,
        width=largura,
        margin=LAYOUT_CONFIG["margem"],
        title=dict(
            text=titulo or "",
            font=dict(size=LAYOUT_CONFIG["fonte_titulo"], color=LAYOUT_CONFIG["cor_primaria"]),
            x=0.5,
            xanchor="center",
        ),
        legend=dict(
            font=dict(size=LAYOUT_CONFIG["fonte_legenda"]),
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
        ),
        font=dict(family=LAYOUT_CONFIG["fonte_base"]),
    )
    return fig


# ---------------------------------------------------------
# 2️⃣ Função para formatar containers Streamlit
# ---------------------------------------------------------
def iniciar_secao(titulo: str, icone: str = "📊"):
    """
    Cria uma seção padronizada para blocos de visualização.

    :param titulo: título da seção
    :param icone: emoji ou ícone de identificação
    """
    st.markdown(f"### {icone} {titulo}")
    st.divider()


# ---------------------------------------------------------
# 3️⃣ Função para prevenir sobreposição de legendas (Plotly/Matplotlib)
# ---------------------------------------------------------
def ajustar_legendas(fig, tipo="plotly"):
    """
    Ajusta a posição de legendas conforme o tipo de gráfico.
    """
    if tipo == "plotly":
        fig.update_layout(legend=dict(yanchor="bottom", y=-0.3))
    elif tipo == "matplotlib":
        import matplotlib.pyplot as plt
        plt.tight_layout(pad=2.0)
    return fig


# ---------------------------------------------------------
# 4️⃣ Função de teste rápido
# ---------------------------------------------------------
def exemplo_visual():
    """Renderiza um exemplo básico no Streamlit (debug)."""
    import plotly.express as px

    df = px.data.gapminder().query("year == 2007")
    fig = px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
    )
    fig = ajustar_grafico(fig, titulo="Exemplo de Gráfico SAAB 5.0")
    st.plotly_chart(fig, use_container_width=True)
    st.success("Visual padrão SAAB 5.0 aplicado com sucesso ✅")
