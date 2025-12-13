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
from home_utils.sidebar_organizer import apply_sidebar_grouping
from datetime import datetime

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(
    page_title="Documentação - Projeto SAAB-Tech",
    layout="wide",
    page_icon="📚"
)
apply_sidebar_grouping()

# --------------------------------------------------------------
# CSS Customizado - Acessibilidade WCAG 2.1 AA (Contraste 4.5:1+)
# --------------------------------------------------------------
st.markdown("""
<style>
    /* Cabeçalho da página - Gradiente azul escuro/vermelho + branco (Contraste: 8.2:1) */
    .doc-header {
        background: linear-gradient(135deg, #003366 0%, #991111 100%);
        padding: 2rem;
        border-radius: 10px;
        color: #FFFFFF;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.15);
    }
    
    .doc-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .doc-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        color: #F0F0F0;
        font-weight: 500;
    }
    
    /* Cards de manual - Fundo claro + texto escuro (Contraste: 12.6:1) */
    .manual-info-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F5F5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #003366;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .manual-info-card h3 {
        color: #002244;
        margin-top: 0;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .manual-info-card p {
        margin: 0.5rem 0;
        color: #1A1A1A;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .manual-info-card p strong {
        color: #002244;
        font-weight: 600;
    }
    
    /* Estilo do conteúdo do manual */
    .manual-content {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #DADADA;
        margin-top: 1rem;
        max-height: 600px;
        overflow-y: auto;
        color: #1A1A1A;
    }
    
    /* Botões de download - Gradiente escuro + branco (Contraste: 8.2:1) */
    .stDownloadButton button {
        background: linear-gradient(135deg, #003366 0%, #991111 100%);
        color: #FFFFFF !important;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 51, 102, 0.2);
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 51, 102, 0.35);
        background: linear-gradient(135deg, #004488 0%, #BB1111 100%);
    }
    
    /* Navegação breadcrumb - Fundo claro + texto escuro (Contraste: 8.1:1) */
    .breadcrumb {
        background: #F8F9FA;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        color: #1A1A1A;
        border: 1px solid #E0E0E0;
    }
    
    .breadcrumb a {
        color: #003366;
        font-weight: 600;
        text-decoration: none;
    }
    
    .breadcrumb a:hover {
        text-decoration: underline;
    }
    
    /* Estatísticas - Azul escuro + branco (Contraste: 9.1:1) */
    .stat-box {
        background: linear-gradient(135deg, #002D5B 0%, #004080 100%);
        color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(0, 45, 91, 0.25);
        transition: transform 0.2s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0, 45, 91, 0.35);
    }
    
    .stat-box h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    .stat-box p {
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
        color: #E8E8E8;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Dicionário de manuais
# --------------------------------------------------------------
MANUAIS = {
    "📘 Manual 01 - Introdução e Primeiros Passos": {
        "arquivo": "MANUAL_01_INTRODUCAO_PRIMEIROS_PASSOS.md",
        "descricao": "Visão geral do sistema, arquitetura, requisitos técnicos e primeiros passos.",
        "paginas": "80-120",
        "nivel": "Iniciante",
        "icone": "📘"
    },
    "📗 Manual 02 - Módulos de Planejamento": {
        "arquivo": "MANUAL_02_MODULOS_PLANEJAMENTO.md",
        "descricao": "Documentação completa dos módulos Insumos, DFD, ETP e TR.",
        "paginas": "60-80",
        "nivel": "Intermediário",
        "icone": "📗"
    },
    "📙 Manual 03 - Edital e Validador": {
        "arquivo": "MANUAL_03_EDITAL_VALIDADOR.md",
        "descricao": "Geração de editais e validação automatizada com score de conformidade.",
        "paginas": "40-50",
        "nivel": "Intermediário",
        "icone": "📙"
    },
    "📕 Manual 04 - Contrato Administrativo": {
        "arquivo": "MANUAL_04_CONTRATO.md",
        "descricao": "Módulo de contrato com 20 campos contratuais e 15 cláusulas DOCX.",
        "paginas": "35-45",
        "nivel": "Intermediário",
        "icone": "📕"
    },
    "📔 Manual 05 - Módulos de Governança": {
        "arquivo": "MANUAL_05_MODULOS_GOVERNANCA.md",
        "descricao": "Sistema de alertas, análise de desempenho, painéis gerenciais e consolidação.",
        "paginas": "30-40",
        "nivel": "Avançado",
        "icone": "📔"
    },
    "📓 Manual 06 - Módulos Avançados": {
        "arquivo": "MANUAL_06_MODULOS_AVANCADOS.md",
        "descricao": "Relatório técnico, comparador, registro de versão e integração com SAJ ADM.",
        "paginas": "30-40",
        "nivel": "Avançado",
        "icone": "📓"
    },
    "📖 Manual 07 - FAQ e Troubleshooting": {
        "arquivo": "MANUAL_07_FAQ_TROUBLESHOOTING.md",
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
            
            # Aviso sobre navegação interna
            st.info("💡 **Dica:** Use Ctrl+F (ou Cmd+F) para buscar seções específicas dentro do manual.")
            
            st.markdown('<div class="manual-content">', unsafe_allow_html=True)
            st.markdown(conteudo, unsafe_allow_html=True)
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
