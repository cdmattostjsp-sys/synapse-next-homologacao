# ==========================================================
# 🏛️ SynapseNext – SAAB 5.0
# Secretaria de Administração e Abastecimento – TJSP
# Página Inicial (Home)
# ==========================================================

import streamlit as st
from pathlib import Path
import sys
import base64

# ==========================================================
# 🔧 Correção de caminho para permitir importações globais
# ==========================================================
# Garante que o diretório raiz do projeto seja visível
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==========================================================
# 📦 Importa o estilo institucional global
# ==========================================================
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional

# ==========================================================
# ⚙️ Configurações da Página
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – SAAB 5.0",
    layout="wide",
    page_icon="🏛️"
)

# ==========================================================
# 🎨 Aplicar estilo institucional global
# ==========================================================
aplicar_estilo_institucional()

# ==========================================================
# 🏛️ Cabeçalho institucional refinado
# ==========================================================
logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"

# CSS local para alinhar o cabeçalho
st.markdown("""
<style>
.cabecalho-tjsp {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 16px;
    margin-top: -10px;
    margin-bottom: 1rem;
}

.cabecalho-tjsp img {
    height: 58px;
    margin-top: -4px;
}

.cabecalho-texto {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.cabecalho-texto h1 {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2b2b2b;
    margin: 0;
    padding: 0;
    line-height: 1.2;
}

.cabecalho-texto h2 {
    font-size: 0.95rem;
    font-weight: 500;
    color: #555;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# Renderização do cabeçalho com logotipo
if logo_path.exists():
    with open(logo_path, "rb") as img_file:
        logo_b64 = base64.b64encode(img_file.read()).decode("utf-8")

    st.markdown(f"""
    <div class="cabecalho-tjsp">
        <img src="data:image/png;base64,{logo_b64}" alt="Logo TJSP">
        <div class="cabecalho-texto">
            <h1>SynapseNext – SAAB 5.0</h1>
            <h2>Ambiente Institucional de Automação da Fase Interna de Licitação</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="cabecalho-tjsp">
        <div class="cabecalho-texto">
            <h1>SynapseNext – SAAB 5.0</h1>
            <h2>Ambiente Institucional de Automação da Fase Interna de Licitação</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧭 Apresentação institucional
# ==========================================================
st.markdown("""
<p style='font-size:0.93rem; text-align:justify;'>
O <b>SynapseNext</b> é um ecossistema digital desenvolvido pela 
<b>Secretaria de Administração e Abastecimento (SAAB)</b> do Tribunal de Justiça de São Paulo,
voltado à automação, padronização e integração dos artefatos que compõem a 
<b>fase interna da licitação</b>, conforme a <b>Lei nº 14.133/2021</b>,
as <b>Resoluções CNJ nº 452/2022</b> e a <b>Instrução Normativa SAAB nº 12/2025</b>.
</p>

<p style='font-size:0.93rem; text-align:justify;'>
O sistema conecta módulos inteligentes e pipelines de governança que abrangem todo o ciclo de elaboração:
<b>DFD → ETP → TR → Edital → Contrato</b>, promovendo segurança jurídica, rastreabilidade e eficiência administrativa.
</p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧩 Funcionalidades principais
# ==========================================================
st.markdown("""
<h3>🌿 Funcionalidades Principais</h3>

<ul style='font-size:0.93rem;'>
<li><b>Criação orientada</b> de artefatos da fase interna (DFD, ETP, TR, Edital e Contrato);</li>
<li><b>Validação automática</b> de coerência e conformidade legal com base nos checklists institucionais;</li>
<li><b>Exportação institucional</b> em formato <code>.docx</code> e <code>.pdf</code> com padronização SAAB/TJSP;</li>
<li><b>Painel Executivo</b> com indicadores de governança, alertas e insights históricos;</li>
<li><b>Integração nativa</b> com SharePoint e OneDrive para armazenamento e versionamento controlado.</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧱 Estrutura Modular
# ==========================================================
st.markdown("""
<h3>🧱 Estrutura Modular</h3>

<p style='font-size:0.93rem; text-align:justify;'>
Cada módulo do SynapseNext está vinculado a um pipeline de auditoria que valida e armazena
os artefatos produzidos, seguindo os parâmetros técnicos da Secretaria de Administração e Abastecimento.
</p>

<p style='font-size:0.93rem; text-align:justify;'>
O sistema permite revisão, versionamento e exportação automatizada dos documentos,
mantendo a rastreabilidade entre todas as fases da fase interna da licitação.
</p>
""", unsafe_allow_html=True)

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
rodape_institucional()
