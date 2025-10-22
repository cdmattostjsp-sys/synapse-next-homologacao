import streamlit as st
from PyPDF2 import PdfReader
import docx
import json
import tempfile
from utils.integration_insumos import process_insumo_text

st.set_page_config(page_title="🔧 Insumos", layout="wide")

st.title("🔧 Gestão de Insumos para Artefatos")
st.caption("Envie documentos base (DFD, ETP, TR, etc.) para pré-processamento e integração automática")

# Funções utilitárias
def extract_text_from_docx(file_path: str) -> str:
    try:
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception:
        return ""

def extract_text_from_pdf(file_path: str) -> str:
    """Lê PDFs com PyPDF2 (já incluído no requirements.txt)"""
    try:
        text = []
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text.append(page.extract_text() or "")
        return "\n".join(text)
    except Exception:
        return ""

# Interface principal
st.subheader("📤 Upload de Documento")
st.markdown("Selecione o tipo de artefato e envie o documento correspondente.")

col1, col2, col3 = st.columns(3)
artefato = col1.selectbox("Tipo de artefato", ["DFD", "ETP", "TR", "Edital", "Contrato"])
descricao = col2.text_input("Descrição do arquivo (opcional)")
autor = col3.text_input("Responsável pelo envio", value="")

uploaded_file = st.file_uploader("Envie o arquivo (.docx ou .pdf)", type=["docx", "pdf"])

if uploaded_file:
    suffix = uploaded_file.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    text = extract_text_from_docx(tmp_path) if suffix == "docx" else extract_text_from_pdf(tmp_path)
    campos_ai = process_insumo_text(text, artefato)

    # Armazenamento em sessão
    st.session_state["last_insumo"] = {
        "nome": uploaded_file.name,
        "artefato": artefato,
        "descricao": descricao,
        "autor": autor,
        "conteudo": text,
        "campos_ai": campos_ai,
    }

    st.success(f"✅ Insumo '{uploaded_file.name}' registrado e processado para o artefato **{artefato}**.")
    st.json(campos_ai)
    st.info("O documento estará automaticamente disponível ao abrir a página do artefato correspondente.")

# Exibição do último insumo ativo
if "last_insumo" in st.session_state:
    insumo = st.session_state["last_insumo"]
    st.divider()
    st.caption(f"🗂️ Último insumo ativo: {insumo['nome']} – artefato {insumo['artefato']}")
    st.text_area("Prévia do conteúdo legível", insumo["conteudo"][:2000], height=200)
