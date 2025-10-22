# ==========================================================
# 🔧 SynapseNext – Módulo de Insumos Institucionais (com integração DFD)
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
import streamlit as st

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – Insumos Institucionais",
    layout="wide",
    page_icon="🔧"
)

# ==========================================================
# 🔧 Ajuste de path
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

# ==========================================================
# 🎨 Estilo institucional
# ==========================================================
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho
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
# 2️⃣ Upload e registro em sessão
# ==========================================================
st.subheader("2️⃣ Enviar Documento de Apoio")

uploaded_file = st.file_uploader(
    "Selecione o arquivo (PDF, DOCX ou TXT)",
    type=["pdf", "docx", "txt"]
)

descricao = st.text_input("Descrição breve do arquivo:")
usuario = st.text_input("Nome do remetente:", value="Anônimo")

if uploaded_file and st.button("📤 Enviar e Registrar", use_container_width=True, type="primary"):
    try:
        # Leitura e armazenamento básico
        file_content = uploaded_file.read().decode("utf-8", errors="ignore")

        st.session_state["insumo_atual"] = {
            "nome_arquivo": uploaded_file.name,
            "conteudo": file_content,
            "artefato": artefato,
            "descricao": descricao.strip(),
            "usuario": usuario.strip(),
        }

        st.success(f"✅ Insumo '{uploaded_file.name}' registrado para o artefato {artefato}.")
        st.info("O documento estará disponível automaticamente ao abrir a página do artefato correspondente (ex.: DFD).")

    except Exception as e:
        st.error(f"❌ Erro ao processar o arquivo: {e}")

st.divider()

# ==========================================================
# 3️⃣ Visualização do último insumo ativo
# ==========================================================
if "insumo_atual" in st.session_state:
    ins = st.session_state["insumo_atual"]
    st.markdown(f"**🗂️ Último insumo ativo:** `{ins['nome_arquivo']}` – artefato `{ins['artefato']}`")
    st.text_area("Prévia do conteúdo", ins["conteudo"][:1000], height=200)
else:
    st.info("Nenhum insumo ativo nesta sessão.")

st.divider()

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
st.caption(
    "SynapseNext – SAAB 5.0 • Módulo de Insumos Institucionais • Integração com DFD ativa."
)
