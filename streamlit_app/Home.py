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
# 🏛️ Cabeçalho institucional ajustado (microalinhamento)
# ==========================================================
logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"

st.markdown("""
<style>
.cabecalho-tjsp {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 18px;
    margin-top: -4px;           /* leve ajuste para centralizar */
    margin-bottom: 1.4rem;
}

.cabecalho-tjsp img {
    height: 70px;
    margin-top: 0px;
}

.cabecalho-texto {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-top: 8px;            /* ↓ aqui está o microajuste que desce o texto */
}

.cabecalho-texto h1 {
    font-size: 1.55rem;
    font-weight: 700;
    color: #2b2b2b;
    margin: 0;
    padding: 0;
    line-height: 1.3;
}

.cabecalho-texto h2 {
    font-size: 0.98rem;
    font-weight: 500;
    color: #555;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

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

# ==========================================================
# 🧭 Apresentação institucional (texto original mantido)
# ==========================================================
st.markdown("""
O **SynapseNext** é um ecossistema digital desenvolvido pela **Secretaria de Administração e Abastecimento (SAAB)** do Tribunal de Justiça de São Paulo, 
destinado a padronizar, auditar e integrar os artefatos que compõem a **fase interna da licitação**, 
de forma automatizada, transparente e aderente à **Lei nº 14.133/2021** e à **Instrução Normativa nº 12/2025**.

Ele conecta módulos inteligentes e pipelines de governança que abrangem todo o ciclo de elaboração:  
**DFD → ETP → TR → Edital → Contrato**, promovendo segurança jurídica, rastreabilidade e eficiência administrativa.
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧩 Funcionalidades principais
# ==========================================================
st.markdown("""
### 🌿 Funcionalidades Principais

- **Criação orientada** de artefatos da fase interna (DFD, ETP, TR, Edital e Contrato);
- **Validação automática** de coerência e conformidade legal com base nos checklists institucionais;
- **Exportação institucional** em formato `.docx` e `.pdf` com padronização SAAB/TJSP;
- **Painel Executivo** com indicadores de governança, alertas e insights históricos;
- **Integração nativa** com SharePoint e OneDrive para armazenamento e versionamento controlado.
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧱 Estrutura Modular
# ==========================================================
st.markdown("""
### 🧱 Estrutura Modular

Cada módulo do SynapseNext está vinculado a um pipeline de auditoria que valida e armazena
os artefatos produzidos, seguindo os parâmetros técnicos da Secretaria de Administração e Abastecimento.

O sistema permite revisão, versionamento e exportação automatizada dos documentos,
mantendo a rastreabilidade entre todas as fases da fase interna da licitação.
""")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
rodape_institucional()
