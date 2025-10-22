import streamlit as st
import os
import base64
import tempfile
import docx
import fitz  # PyMuPDF
import re
import json
from pathlib import Path
from openai import OpenAI

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(page_title="🔧 Insumos", layout="wide")
st.title("🔧 Insumos – Central de Documentos Base")
st.caption("Upload de documentos de apoio e extração semântica automática para artefatos institucionais.")

# ==========================================================
# 📦 Conexão com OpenAI
# ==========================================================
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# ==========================================================
# 📂 Funções utilitárias
# ==========================================================
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(file) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_sections(text):
    """
    Divide o texto em seções numeradas (1. Título ... 2. Próximo título ...)
    Captura multilinhas até o próximo número.
    """
    sections = re.split(r"\n\s*\d+\.\s*(?=[A-ZÁÉÍÓÚ])", text)
    result = {}
    for sec in sections:
        if not sec.strip():
            continue
        header_match = re.match(r"([A-Za-zÁÉÍÓÚâêôçãõ\s\-]+)\n", sec)
        if header_match:
            title = header_match.group(1).strip()
            content = sec[len(title):].strip()
            result[title] = content
    return result

def analyze_with_ai(text):
    prompt = f"""
Você é um analista técnico encarregado de extrair informações institucionais de um Documento de Formalização da Demanda (DFD).
Retorne um JSON com os seguintes campos se forem encontrados:

- unidade
- responsavel
- objeto
- justificativa
- quantidade
- urgencia
- riscos
- alinhamento

Texto de referência:
{text[:7000]}
"""
    response = client.chat.completions.create(
        model=st.secrets["openai"]["model"],
        messages=[{"role": "system", "content": "Você é um extrator de informações técnicas."},
                  {"role": "user", "content": prompt}]
    )
    try:
        data = json.loads(response.choices[0].message.content)
    except Exception:
        data = {"resposta_bruta": response.choices[0].message.content}
    return data

# ==========================================================
# 🧾 Upload e processamento
# ==========================================================
with st.form("upload_form"):
    artefato = st.selectbox("Selecione o artefato de destino", ["DFD", "TR", "Edital", "Contrato"])
    uploaded_file = st.file_uploader("Envie um documento (.docx ou .pdf)", type=["docx", "pdf"])
    descricao = st.text_input("Descrição do arquivo")
    anotante = st.text_input("Nome do responsável pelo envio")
    submitted = st.form_submit_button("📤 Enviar e processar")

if submitted and uploaded_file:
    with st.spinner("Processando o documento..."):
        suffix = Path(uploaded_file.name).suffix.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        text = extract_text_from_docx(tmp_path) if suffix == ".docx" else extract_text_from_pdf(tmp_path)
        sections = extract_sections(text)
        ai_result = analyze_with_ai(text)

        st.session_state["last_insumo"] = {
            "artefato": artefato,
            "nome": uploaded_file.name,
            "descricao": descricao,
            "anotante": anotante,
            "conteudo": text,
            "secoes": sections,
            "campos_ai": ai_result,
        }

        st.success(f"Insumo '{uploaded_file.name}' registrado e processado para o artefato {artefato}.")
        st.info("📎 O documento estará disponível automaticamente ao abrir a página do artefato correspondente.")

if "last_insumo" in st.session_state:
    insumo = st.session_state["last_insumo"]
    st.divider()
    st.subheader("📊 Resultado do processamento")
    st.json(insumo["campos_ai"])
    st.write("🗂️ Último insumo ativo:", f"{insumo['nome']} – artefato {insumo['artefato']}")
    with st.expander("Prévia do conteúdo legível"):
        st.text(insumo["conteudo"][:2000])
