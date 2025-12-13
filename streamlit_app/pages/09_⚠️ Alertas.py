import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# ⚠️ SynapseNext – Painel de Alertas v2025.1 (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Exibir alertas institucionais e pendências detectadas
#   nas etapas do fluxo de contratação pública (Lei 14.133/2021).
#   
#   VERSÃO 2025.1 - SISTEMA FUNCIONAL:
#   - Coleta dados REAIS dos documentos processados
#   - Valida campos obrigatórios (21 campos em 5 módulos)
#   - Detecta inconsistências entre DFD/ETP/TR/Edital/Contrato
#   - Histórico de alertas anteriores
#   - Filtros por módulo e severidade
# ==========================================================

import streamlit as st
from home_utils.sidebar_organizer import apply_sidebar_grouping
import plotly.express as px
import pandas as pd
from datetime import datetime
import sys, os

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional
from utils.alertas_pipeline import gerar_alertas_reais, carregar_historico, obter_estatisticas_historico

# Configuração da página Streamlit
st.set_page_config(page_title="⚠️ Alertas – SynapseNext", layout="wide")
apply_sidebar_grouping()
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">⚠️ Painel de Alertas</h1>
    <p style="color:#4d4d4d; font-size:1rem;">Monitoramento de pendências e inconsistências – SAAB/TJSP</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# 🔄 Botão: Atualizar Alertas
# ==========================================================
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    if st.button("🔄 Atualizar Alertas", use_container_width=True, type="primary"):
        with st.spinner("🔍 Coletando estado dos documentos..."):
            resultado = gerar_alertas_reais(salvar_historico=True)
            st.success(f"✅ {resultado['totais']['total']} alertas detectados!")
            st.rerun()

# ==========================================================
# 📊 Gerar Alertas Reais do Sistema
# ==========================================================
if "alertas_cache" not in st.session_state:
    with st.spinner("🔍 Coletando alertas do sistema..."):
        resultado = gerar_alertas_reais(salvar_historico=False)
        st.session_state.alertas_cache = resultado

resultado = st.session_state.alertas_cache
alertas = resultado.get("alerts", [])
totais = resultado.get("totais", {})

# ==========================================================
# 📌 Cards de resumo REAIS
# ==========================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚨 Críticos", totais.get("critico", 0), "Pendências graves")
with col2:
    st.metric("⚠️ Médios", totais.get("medio", 0), "Atenção necessária")
with col3:
    st.metric("ℹ️ Informativos", totais.get("informativo", 0), "Avisos gerais")

st.markdown("")

# ==========================================================
# 🔍 Filtros na Sidebar
# ==========================================================
st.sidebar.markdown("### 🔍 Filtros")

modulos_disponiveis = sorted(set([a.get("modulo", "SISTEMA") for a in alertas]))
modulos_filtro = st.sidebar.multiselect(
    "Módulos",
    options=modulos_disponiveis,
    default=modulos_disponiveis,
)

severidades_disponiveis = ["alto", "medio", "baixo"]
severidade_filtro = st.sidebar.multiselect(
    "Severidade",
    options=severidades_disponiveis,
    default=severidades_disponiveis,
)

# Aplicar filtros
alertas_filtrados = [
    a for a in alertas 
    if a.get("modulo") in modulos_filtro 
    and a.get("severidade") in severidade_filtro
]

# ==========================================================
# 📈 Gráfico de distribuição dos alertas REAIS
# ==========================================================
if alertas_filtrados:
    df_grafico = pd.DataFrame({
        "Tipo": [a.get("tipo", "Informativo") for a in alertas_filtrados],
    })
    contagem = df_grafico["Tipo"].value_counts().reset_index()
    contagem.columns = ["Tipo", "Quantidade"]
    
    fig = px.bar(
        contagem,
        x="Tipo",
        y="Quantidade",
        color="Tipo",
        text_auto=True,
        title=f"Distribuição de Alertas ({len(alertas_filtrados)} total)",
        color_discrete_map={
            "Crítico": "#c0392b",
            "Médio": "#f39c12",
            "Informativo": "#2980b9",
        }
    )
    
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        font=dict(size=13),
        height=420,
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("✅ Nenhum alerta encontrado com os filtros selecionados")

# ==========================================================
# 🧾 Detalhamento dos alertas ativos REAIS
# ==========================================================
st.markdown("### 🔍 Detalhamento dos Alertas Ativos")

if alertas_filtrados:
    for i, alert in enumerate(alertas_filtrados):
        tipo = alert.get("tipo", "Informativo")
        color = "#c0392b" if tipo == "Crítico" else "#f39c12" if tipo == "Médio" else "#2980b9"
        
        modulo = alert.get("modulo", "SISTEMA")
        cor_badge = {
            "DFD": "#3498db",
            "ETP": "#9b59b6",
            "TR": "#e74c3c",
            "EDITAL": "#f39c12",
            "CONTRATO": "#16a085",
            "SISTEMA": "#95a5a6",
        }.get(modulo, "#95a5a6")
        
        st.markdown(
            f"""
            <div style="
                background-color:{color}20;
                border-left:6px solid {color};
                border-radius:8px;
                padding:0.8rem 1rem;
                margin-bottom:0.6rem;
            ">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="background-color:{cor_badge};color:white;padding:0.2rem 0.6rem;border-radius:4px;font-size:0.75rem;font-weight:bold;">{modulo}</span>
                        <strong style="color:{color};margin-left:0.5rem;">{tipo}</strong>
                    </div>
                    <div style="font-size:0.85rem;color:#666;">{alert.get('timestamp', 'N/A')}</div>
                </div>
                <div style="margin-top:0.5rem;font-size:0.95rem;">
                    {alert.get('mensagem', 'Sem mensagem')}
                </div>
                <div style="margin-top:0.4rem;font-size:0.85rem;color:#555;font-style:italic;">
                    💡 {alert.get('recomendacao', 'Sem recomendação')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.success("✅ Nenhum alerta ativo no momento!")

# ==========================================================
# 📜 Histórico de Alertas Anteriores
# ==========================================================
st.markdown("---")
with st.expander("📜 Histórico de Alertas Anteriores (Últimas 10 Execuções)"):
    historico = carregar_historico(limit=10)
    
    if historico:
        st.markdown(f"**Total de execuções no histórico:** {len(historico)}")
        st.markdown("")
        
        for i, hist in enumerate(historico, 1):
            timestamp = hist.get("timestamp", "N/A")
            totais_hist = hist.get("totais", {})
            resumo = hist.get("resumo", "")
            
            col_num, col_data, col_resumo = st.columns([1, 3, 8])
            with col_num:
                st.markdown(f"**#{i}**")
            with col_data:
                st.markdown(f"`{timestamp}`")
            with col_resumo:
                st.markdown(f"{resumo}")
    else:
        st.info("📭 Nenhum histórico disponível ainda")

# ==========================================================
# 📊 Estatísticas do Histórico
# ==========================================================
with st.expander("📊 Estatísticas do Sistema de Alertas"):
    stats = obter_estatisticas_historico()
    
    if stats.get("total_execucoes", 0) > 0:
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Total de Execuções", stats.get("total_execucoes", 0))
        with col_stat2:
            st.metric("Média Alertas Críticos", f"{stats.get('media_alertas_criticos', 0):.1f}")
        with col_stat3:
            st.metric("Média Alertas Total", f"{stats.get('media_alertas_total', 0):.1f}")
        
        st.markdown("")
        st.markdown(f"**Primeira execução:** `{stats.get('primeira_execucao', 'N/A')}`")
        st.markdown(f"**Última execução:** `{stats.get('ultima_execucao', 'N/A')}`")
    else:
        st.info("📭 Nenhuma estatística disponível ainda")

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
rodape_institucional()
