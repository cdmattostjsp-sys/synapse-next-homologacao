import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# 💡 SynapseNext – Painel de Análise de Desempenho v2025.1 (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Exibir métricas de desempenho técnico e consistência
#   documental com visual padronizado SAAB 5.0.
#   
#   VERSÃO 2025.1 - SISTEMA FUNCIONAL:
#   - Coleta dados REAIS de auditoria (word_count, timestamps)
#   - Métricas de coerência entre documentos
#   - Conformidade legal dos artefatos
#   - Evolução temporal (volume, word count, distribuição)
#   - Histórico de métricas anteriores
#   - Filtros temporais (7, 15, 30 dias)
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys, os

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional
from utils.analytics_pipeline import gerar_metricas_desempenho, carregar_historico_desempenho, obter_estatisticas_historico

st.set_page_config(page_title="💡 Análise de Desempenho – SynapseNext", layout="wide")
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">💡 Análise de Desempenho</h1>
    <p style="color:#4d4d4d; font-size:1rem;">Indicadores técnicos e métricas institucionais – SAAB/TJSP</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# 🔍 Filtros na Sidebar
# ==========================================================
st.sidebar.markdown("### ⚙️ Configurações")

periodo_opcoes = {
    "7 dias": 7,
    "15 dias": 15,
    "30 dias": 30,
    "60 dias": 60,
}
periodo_selecionado = st.sidebar.selectbox(
    "Período de Análise",
    options=list(periodo_opcoes.keys()),
    index=2,  # 30 dias por padrão
)
dias = periodo_opcoes[periodo_selecionado]

# ==========================================================
# 🔄 Botão: Atualizar Métricas
# ==========================================================
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    if st.button("🔄 Atualizar Métricas", use_container_width=True, type="primary"):
        with st.spinner("📊 Coletando métricas do sistema..."):
            metricas = gerar_metricas_desempenho(dias=dias, salvar_historico=True)
            st.session_state.metricas_cache = metricas
            st.success(f"✅ Métricas atualizadas ({metricas['resumo']['total_eventos']} eventos)")
            st.rerun()

# ==========================================================
# 📊 Gerar Métricas Reais do Sistema
# ==========================================================
if "metricas_cache" not in st.session_state:
    with st.spinner("📊 Coletando métricas do sistema..."):
        metricas = gerar_metricas_desempenho(dias=dias, salvar_historico=False)
        st.session_state.metricas_cache = metricas

metricas = st.session_state.metricas_cache
resumo = metricas.get("resumo", {})
evolucao = metricas.get("evolucao_temporal", {})

# Verificar se há dados de auditoria reais ou sintéticos
tem_eventos = resumo.get("total_eventos", 0) > 0
if tem_eventos:
    # Verificar se são dados sintéticos (word_count muito baixo indica isso)
    word_count_medio = resumo.get("word_count_medio", 0)
    if word_count_medio < 100:
        st.info("ℹ️ **Modo Sintético**: O sistema de auditoria não foi encontrado. Exibindo métricas baseadas nos documentos processados. Para dados mais detalhados, execute os documentos com o sistema de auditoria ativado.")
else:
    st.warning("⚠️ Nenhum dado disponível para análise. Processe documentos através dos módulos DFD, ETP, TR, EDITAL ou CONTRATO.")

# ==========================================================
# 📌 Cards de resumo REAIS
# ==========================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📄 Total Eventos", resumo.get("total_eventos", 0), "Processamentos")
with col2:
    st.metric("📝 Word Count Total", f"{resumo.get('total_word_count', 0):,}", "Palavras")
with col3:
    st.metric("✅ Conformidade", f"{resumo.get('conformidade_percentual', 0):.1f}%", "Legal")
with col4:
    st.metric("🧩 Coerência", f"{resumo.get('coerencia_global_atual', 0):.1f}%", "Global")

st.markdown("")

# ==========================================================
# 📊 Seção 1 – Evolução temporal (Volume total) REAL
# ==========================================================
st.subheader("📈 Evolução temporal – Volume de eventos")

volume_dados = evolucao.get("volume_eventos", [])
if volume_dados:
    df_volume = pd.DataFrame(volume_dados)
    fig_vol = px.line(
        df_volume, x="data", y="valor", markers=True,
        title=f"Volume total de eventos registrados ({periodo_selecionado})",
        line_shape="spline"
    )
    fig_vol.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        font=dict(size=13),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig_vol, use_container_width=True)
else:
    st.info("📭 Nenhum dado de volume disponível no período selecionado")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🗂️ Seção 2 – Volume por artefato REAL
# ==========================================================
st.subheader("📁 Distribuição de eventos por artefato")

distribuicao_modulos = evolucao.get("distribuicao_modulos", {})
if distribuicao_modulos:
    # Construir dataframe long para plotly
    rows = []
    for modulo, dados_modulo in distribuicao_modulos.items():
        for ponto in dados_modulo:
            rows.append({
                "data": ponto["data"],
                "Artefato": modulo,
                "Eventos": ponto["valor"]
            })
    
    if rows:
        df_art_long = pd.DataFrame(rows)
        fig_art = px.line(
            df_art_long, x="data", y="Eventos", color="Artefato", markers=True,
            title=f"Evolução por Artefato ({periodo_selecionado})"
        )
        fig_art.update_layout(
            title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
            font=dict(size=13),
            height=400,
            legend_title_text="Artefato",
            margin=dict(l=20, r=20, t=60, b=40)
        )
        st.plotly_chart(fig_art, use_container_width=True)
    else:
        st.info("📭 Nenhum dado de distribuição disponível no período selecionado")
else:
    st.info("📭 Nenhum dado de distribuição disponível no período selecionado")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🧭 Seção 3 – Coerência global REAL
# ==========================================================
st.subheader("🧭 Tendência de coerência global")

coerencia_dados = metricas.get("coerencia", {})
historico_coerencia = coerencia_dados.get("historico", [])

if historico_coerencia:
    # Preparar dados para gráfico
    coerencia_plot = []
    for registro in historico_coerencia[-30:]:  # Últimos 30 registros
        timestamp = registro.get("timestamp", "")
        data = timestamp.split("T")[0] if "T" in timestamp else timestamp[:10]
        coerencia_plot.append({
            "data": data,
            "valor": registro.get("coerencia_global", 0)
        })
    
    df_coer = pd.DataFrame(coerencia_plot)
    fig_coer = px.line(
        df_coer, x="data", y="valor", markers=True, color_discrete_sequence=["#00A86B"],
        title="Índice de Coerência Global (%)"
    )
    fig_coer.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        yaxis=dict(range=[0, 100]),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig_coer, use_container_width=True)
else:
    st.info("📭 Nenhum dado de coerência disponível. Execute análises de comparação entre documentos.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📄 Seção 4 – Tamanho médio dos artefatos REAL (WordCount)
# ==========================================================
st.subheader("📄 Evolução do tamanho médio (WordCount)")

word_count_dados = evolucao.get("word_count_total", [])
if word_count_dados:
    df_wc = pd.DataFrame(word_count_dados)
    fig_wc = px.line(
        df_wc, x="data", y="valor", markers=True, color_discrete_sequence=["#6A0DAD"],
        title=f"Total de palavras por dia ({periodo_selecionado})"
    )
    fig_wc.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig_wc, use_container_width=True)
else:
    st.info("📭 Nenhum dado de word count disponível no período selecionado")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📉 Seção 5 – Estatísticas por Artefato REAL
# ==========================================================
st.subheader("📉 Estatísticas detalhadas por Artefato")

distribuicao_artefatos = metricas.get("distribuicao_artefatos", {})
if distribuicao_artefatos:
    dados_tabela = []
    for modulo, stats in distribuicao_artefatos.items():
        dados_tabela.append({
            "Artefato": modulo,
            "Total Eventos": stats.get("total_eventos", 0),
            "Word Count Total": stats.get("word_count_total", 0),
            "Word Count Médio": f"{stats.get('word_count_medio', 0):.0f}",
            "Último Processamento": stats.get("ultimo_processamento", "N/A")[:19] if stats.get("ultimo_processamento") else "N/A",
        })
    
    df_stats = pd.DataFrame(dados_tabela)
    st.dataframe(df_stats, use_container_width=True, hide_index=True)
else:
    st.info("📭 Nenhuma estatística de artefatos disponível")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📜 Histórico de Métricas Anteriores
# ==========================================================
st.markdown("---")
with st.expander("📜 Histórico de Métricas Anteriores (Últimas 30 Execuções)"):
    historico = carregar_historico_desempenho(limit=30)
    
    if historico:
        st.markdown(f"**Total de execuções no histórico:** {len(historico)}")
        st.markdown("")
        
        for i, hist in enumerate(historico, 1):
            timestamp = hist.get("timestamp", "N/A")
            eventos = hist.get("total_eventos", 0)
            conformidade = hist.get("conformidade", 0)
            coerencia = hist.get("coerencia", 0)
            
            col_num, col_data, col_info = st.columns([1, 3, 8])
            with col_num:
                st.markdown(f"**#{i}**")
            with col_data:
                st.markdown(f"`{timestamp}`")
            with col_info:
                st.markdown(f"Eventos: **{eventos}** | Conformidade: **{conformidade:.1f}%** | Coerência: **{coerencia:.1f}%**")
    else:
        st.info("📭 Nenhum histórico disponível ainda")

# ==========================================================
# 📊 Estatísticas do Histórico
# ==========================================================
with st.expander("📊 Estatísticas do Sistema de Análise"):
    stats = obter_estatisticas_historico()
    
    if stats.get("total_execucoes", 0) > 0:
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Execuções", stats.get("total_execucoes", 0))
        with col_stat2:
            st.metric("Média Eventos", f"{stats.get('media_eventos', 0):.1f}")
        with col_stat3:
            st.metric("Média Conformidade", f"{stats.get('media_conformidade', 0):.1f}%")
        with col_stat4:
            st.metric("Média Coerência", f"{stats.get('media_coerencia', 0):.1f}%")
        
        st.markdown("")
        st.markdown(f"**Primeira execução:** `{stats.get('primeira_execucao', 'N/A')}`")
        st.markdown(f"**Última execução:** `{stats.get('ultima_execucao', 'N/A')}`")
    else:
        st.info("📭 Nenhuma estatística disponível ainda")

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
rodape_institucional()
