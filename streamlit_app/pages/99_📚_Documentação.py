# -*- coding: utf-8 -*-
# ==============================================================
# Projeto SAAB-Tech
# Página de Documentação do Sistema
# ==============================================================
# Versão institucional v1 – Dezembro/2025
# ==============================================================

# --------------------------------------------------------------
# 🔧 Correção de contexto de execução para Streamlit Cloud
# --------------------------------------------------------------
import sys
from pathlib import Path

# Garante que a pasta raiz do projeto seja reconhecida pelo Python
base_path = Path(__file__).resolve().parents[2]
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))

# --------------------------------------------------------------
# Imports principais
# --------------------------------------------------------------
import streamlit as st
from datetime import datetime

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(
    page_title="Documentação - Projeto SAAB-Tech",
    layout="wide",
    page_icon="📚"
)

# --------------------------------------------------------------
# CSS Customizado
# --------------------------------------------------------------
st.markdown("""
<style>
    /* Cabeçalho da página */
    .doc-header {
        background: linear-gradient(135deg, rgb(0,51,102) 0%, #990000 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .doc-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .doc-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Cards de manual */
    .manual-info-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid rgb(0,51,102);
        margin-bottom: 1.5rem;
    }
    
    .manual-info-card h3 {
        color: rgb(0,51,102);
        margin-top: 0;
        font-size: 1.4rem;
    }
    
    .manual-info-card p {
        margin: 0.5rem 0;
        color: #333;
    }
    
    /* Estilo do conteúdo do manual */
    .manual-content {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-top: 1rem;
        max-height: 600px;
        overflow-y: auto;
    }
    
    /* Botões de download */
    .stDownloadButton button {
        background: linear-gradient(135deg, rgb(0,51,102) 0%, #990000 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,51,102,0.3);
    }
    
    /* Navegação breadcrumb */
    .breadcrumb {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    
    /* Estatísticas */
    .stat-box {
        background: linear-gradient(135deg, rgb(0,51,102) 0%, #003d7a 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stat-box h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stat-box p {
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Dicionário de manuais
# --------------------------------------------------------------
MANUAIS = {
    "📘 Manual 01 - Introdução e Primeiros Passos": {
        "arquivo": "MANUAL_01_INTRODUCAO.md",
        "descricao": "Visão geral do sistema, arquitetura, requisitos técnicos e primeiros passos.",
        "paginas": "80-120",
        "nivel": "Iniciante",
        "icone": "📘"
    },
    "📗 Manual 02 - Módulos de Planejamento": {
        "arquivo": "MANUAL_02_PLANEJAMENTO.md",
        "descricao": "Documentação completa dos módulos Insumos, DFD, ETP e TR.",
        "paginas": "60-80",
        "nivel": "Intermediário",
        "icone": "📗"
    },
    "📙 Manual 03A - Edital e Validador": {
        "arquivo": "MANUAL_03A_EDITAL.md",
        "descricao": "Geração de editais e validação automatizada com score de conformidade.",
        "paginas": "40-50",
        "nivel": "Intermediário",
        "icone": "📙"
    },
    "📕 Manual 03B - Contrato Administrativo": {
        "arquivo": "MANUAL_03B_CONTRATO.md",
        "descricao": "Módulo de contrato com 20 campos contratuais e 15 cláusulas DOCX.",
        "paginas": "35-45",
        "nivel": "Intermediário",
        "icone": "📕"
    },
    "📔 Manual 04 - Módulos de Governança": {
        "arquivo": "MANUAL_04_MODULOS_GOVERNANCA.md",
        "descricao": "Sistema de alertas, análise de desempenho, painéis gerenciais e consolidação.",
        "paginas": "30-40",
        "nivel": "Avançado",
        "icone": "📔"
    },
    "📓 Manual 05 - Módulos Avançados": {
        "arquivo": "MANUAL_05_MODULOS_AVANCADOS.md",
        "descricao": "Relatório técnico, comparador, registro de versão e integração com SAJ ADM.",
        "paginas": "30-40",
        "nivel": "Avançado",
        "icone": "📓"
    },
    "📖 Manual 06 - FAQ e Troubleshooting": {
        "arquivo": "MANUAL_06_FAQ_TROUBLESHOOTING.md",
        "descricao": "20 perguntas frequentes, soluções de problemas e recursos de suporte.",
        "paginas": "30-40",
        "nivel": "Todos",
        "icone": "📖"
    }
}

# --------------------------------------------------------------
# Cabeçalho da página
# --------------------------------------------------------------
st.markdown("""
<div class="doc-header">
    <h1>📚 Documentação do Sistema</h1>
    <p>Central de Manuais do Projeto SAAB-Tech</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Breadcrumb de navegação
# --------------------------------------------------------------
st.markdown("""
<div class="breadcrumb">
    🏠 <a href="/" target="_self">Home</a> → 📚 Documentação
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Estatísticas dos manuais
# --------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-box">
        <h3>7</h3>
        <p>Manuais Disponíveis</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <h3>16</h3>
        <p>Módulos Documentados</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <h3>300+</h3>
        <p>Páginas de Conteúdo</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-box">
        <h3>2025.1</h3>
        <p>Versão do Sistema</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# Seletor de manual
# --------------------------------------------------------------
st.markdown("### 📖 Selecione o Manual")

manual_selecionado = st.selectbox(
    "Escolha o manual que deseja consultar:",
    options=list(MANUAIS.keys()),
    format_func=lambda x: x,
    label_visibility="collapsed"
)

# --------------------------------------------------------------
# Informações do manual selecionado
# --------------------------------------------------------------
if manual_selecionado:
    info_manual = MANUAIS[manual_selecionado]
    
    # Card com informações
    st.markdown(f"""
    <div class="manual-info-card">
        <h3>{info_manual['icone']} {manual_selecionado.replace(info_manual['icone'] + ' ', '')}</h3>
        <p><strong>📄 Descrição:</strong> {info_manual['descricao']}</p>
        <p><strong>📏 Páginas:</strong> {info_manual['paginas']} | <strong>🎯 Nível:</strong> {info_manual['nivel']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --------------------------------------------------------------
    # Carregamento e exibição do conteúdo
    # --------------------------------------------------------------
    caminho_manual = base_path / "manuais" / info_manual['arquivo']
    
    if caminho_manual.exists():
        # Tabs para visualização e download
        tab1, tab2 = st.tabs(["👁️ Visualizar", "📥 Download"])
        
        with tab1:
            # Lê e exibe o conteúdo
            with open(caminho_manual, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            st.markdown('<div class="manual-content">', unsafe_allow_html=True)
            st.markdown(conteudo)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 📥 Baixar Manual")
            st.markdown(f"""
            Faça o download do **{manual_selecionado}** para consulta offline.
            
            **Formato:** Markdown (.md)  
            **Tamanho:** {info_manual['paginas']} páginas  
            **Compatível com:** Editores de texto, visualizadores Markdown
            """)
            
            # Botão de download
            with open(caminho_manual, 'rb') as f:
                st.download_button(
                    label=f"⬇️ Baixar {info_manual['arquivo']}",
                    data=f,
                    file_name=info_manual['arquivo'],
                    mime="text/markdown",
                    use_container_width=True
                )
    else:
        st.error(f"❌ Manual não encontrado: `{info_manual['arquivo']}`")
        st.info("Entre em contato com o suporte técnico.")

# --------------------------------------------------------------
# Seção de ajuda adicional
# --------------------------------------------------------------
st.markdown("<br><hr><br>", unsafe_allow_html=True)

st.markdown("### 💡 Precisa de Mais Ajuda?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📧 Suporte Técnico**
    
    saab-tech@tjsp.jus.br
    
    Resposta em até 4 horas úteis
    """)

with col2:
    st.markdown("""
    **🎓 Treinamentos**
    
    Presencial, Online e EAD
    
    Certificação disponível
    """)

with col3:
    st.markdown("""
    **📞 Contato Direto**
    
    (11) XXXX-XXXX
    
    Seg-Sex: 9h-18h
    """)

# --------------------------------------------------------------
# Rodapé
# --------------------------------------------------------------
st.markdown("<br><hr>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    **© 2025 – Tribunal de Justiça do Estado de São Paulo**  
    Projeto SAAB-Tech | Ecossistema SAAB 5.0
    """)

with col2:
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"*Atualizado em {timestamp}*")
