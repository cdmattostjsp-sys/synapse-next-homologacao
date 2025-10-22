# ==========================================================
# 🔧 SynapseNext – Módulo de Insumos Institucionais
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
import streamlit as st

# ==========================================================
# ⚙️ Configuração da página (deve ser o primeiro comando Streamlit)
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – Insumos Institucionais",
    layout="wide",
    page_icon="🔧"
)

# ==========================================================
# 🔧 Setup de caminho
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
try:
    from utils.integration_insumos import salvar_insumo, listar_insumos
except Exception as e:
    st.error(f"❌ Erro ao importar integração de insumos: {e}")
    st.stop()

try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

# ==========================================================
# 🎨 Aplicar estilo global
# ==========================================================
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Insumos Institucionais",
    "Central de upload e controle de documentos auxiliares de cada artefato"
)
st.divider()

# ==========================================================
# 1️⃣ Seleção do artefato
# ==========================================================
st.subheader("1️⃣ Selecione o artefato de destino")

artefato = st.selectbox(
    "Escolha o artefato relacionado ao insumo:",
    ["DFD", "ETP", "TR", "Edital", "Contrato"],
    help="Selecione o artefato para o qual o documento servirá de insumo."
)

# ==========================================================
# 2️⃣ Upload do arquivo
# ==========================================================
st.subheader("2️⃣ Enviar Documento de Apoio")

uploaded_file = st.file_uploader(
    "Selecione o arquivo de apoio (PDF, DOCX, XLSX)...",
    type=["pdf", "docx", "xlsx"]
)

descricao = st.text_input("Descrição breve do arquivo:")
usuario = st.text_input("Nome do remetente:", value="Anônimo")

if uploaded_file and st.button("📤 Enviar Arquivo", type="primary", use_container_width=True):
    try:
        resultado = salvar_insumo(
            artefato,
            uploaded_file,
            usuario=usuario.strip() or "Anônimo",
            descricao=descricao.strip()
        )
        st.success(resultado["mensagem"])
    except Exception as e:
        st.error(f"❌ Erro ao salvar arquivo: {e}")

st.divider()

# ==========================================================
# 3️⃣ Listagem dos arquivos existentes
# ==========================================================
st.subheader("3️⃣ Arquivos armazenados")

try:
    arquivos = listar_insumos(artefato)
    if arquivos:
        st.markdown(f"**Arquivos encontrados em `{artefato}`:**")
        for nome in arquivos:
            st.markdown(f"- 📎 {nome}")
    else:
        st.info("Nenhum arquivo encontrado para este artefato.")
except Exception as e:
    st.error(f"Erro ao listar arquivos: {e}")

st.divider()

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.caption(
    "SynapseNext – SAAB 5.0 • Módulo de Insumos Institucionais • Fase São Paulo (vNext)  \n"
    "Permite o envio e rastreamento de documentos de apoio vinculados aos artefatos da jornada de contratação."
)
