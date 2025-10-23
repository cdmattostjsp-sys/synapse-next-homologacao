# ==============================
# pages/01_🔧 Insumos.py  –  SynapseNext / SAAB TJSP
# ==============================

import streamlit as st
st.set_page_config(page_title="🔧 Insumos", layout="wide")

from datetime import datetime
from io import BytesIO
from pathlib import Path
import sys, os, docx2txt, fitz  # PyMuPDF

# ==========================================================
# 🔍 Importação compatível com a estrutura SynapseNext
# ==========================================================
try:
    from utils.integration_insumos import salvar_insumo, listar_insumos, process_insumo_text
except ModuleNotFoundError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, base_dir)
    from utils.integration_insumos import salvar_insumo, listar_insumos, process_insumo_text

# ==========================================================
# 🏛️ Cabeçalho
# ==========================================================
st.markdown(
    """
    <div style='padding:1.2rem 0;text-align:center;'>
        <h1 style='color:#800000;margin-bottom:0.3rem;'>🔧 Upload de Insumos Institucionais</h1>
        <p style='font-size:1.05rem;color:#444;'>Integração inteligente entre artefatos e dados do SynapseNext</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
O módulo **INSUMOS** permite anexar documentos institucionais (DFD, ETP, TR, Edital, Contrato etc.)  
que servirão de base para os artefatos gerados automaticamente pelo SynapseNext.  
Cada upload é registrado e o conteúdo pode ser processado semanticamente pela IA  
para preenchimento inteligente dos formulários correspondentes.
"""
)

# ==========================================================
# 📂 Upload de documento
# ==========================================================
st.divider()
st.subheader("📎 Enviar novo insumo")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    artefato = st.selectbox("Artefato relacionado", ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"])
with col2:
    descricao = st.text_input("Descrição / Observação", placeholder="Ex: Estudo técnico preliminar revisado")
with col3:
    usuario = st.text_input("Nome do remetente", placeholder="Ex: Carlos Mattos")

arquivo = st.file_uploader("Selecione o arquivo (DOCX, PDF, TXT, etc.)", type=["docx", "pdf", "txt"])

if arquivo and st.button("📤 Enviar insumo"):
    with st.spinner("Salvando e processando o documento..."):
        caminho_salvo = salvar_insumo(arquivo, artefato)
        st.success(f"Insumo '{arquivo.name}' salvo com sucesso em {caminho_salvo}")

        # 🔍 Extração de texto
        texto_extraido = ""
        try:
            nome = arquivo.name.lower()
            arquivo.seek(0)
            dados = arquivo.read()
            if nome.endswith(".pdf"):
                pdf = fitz.open(stream=dados, filetype="pdf")
                texto_extraido = "".join(p.get_text() for p in pdf)
            elif nome.endswith(".docx"):
                texto_extraido = docx2txt.process(BytesIO(dados))
            elif nome.endswith(".txt"):
                texto_extraido = dados.decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"Erro ao extrair texto do arquivo: {e}")

        # 🤖 Processamento IA
        campos_ai = {}
        if texto_extraido.strip():
            st.info("IA processando o insumo e identificando campos relevantes...")
            try:
                dados_inferidos = process_insumo_text(texto_extraido)
                st.success(f"✅ Insumo '{arquivo.name}' registrado e processado com sucesso.")
                st.json(dados_inferidos)
                if isinstance(dados_inferidos, dict):
                    campos_ai = dados_inferidos
            except Exception as e:
                st.error(f"Erro no processamento IA: {e}")
        else:
            st.warning("⚠️ Não foi possível extrair texto legível do arquivo enviado.")

        st.session_state["last_insumo"] = {
            "nome": arquivo.name,
            "artefato": artefato,
            "conteudo": (texto_extraido or "")[:100000],
            "campos_ai": campos_ai,
            "usuario": usuario,
            "descricao": descricao,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        st.info("📎 Insumo ativo armazenado na sessão e disponível para o DFD/TR.")

# ==========================================================
# 🗂️ Histórico de uploads
# ==========================================================
st.divider()
st.subheader("🗂️ Histórico de Insumos Enviados")

artefato_hist = st.selectbox("Filtrar por artefato", ["Todos", "DFD", "ETP", "TR", "EDITAL", "CONTRATO"])

if artefato_hist == "Todos":
    for tipo in ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]:
        arquivos = listar_insumos(tipo)
        st.markdown(f"#### 📘 {tipo} ({len(arquivos)} arquivos)")
        st.write(arquivos or "— sem arquivos —")
else:
    arquivos = listar_insumos(artefato_hist)
    st.markdown(f"#### 📘 {artefato_hist} ({len(arquivos)} arquivos)")
    st.write(arquivos or "Nenhum insumo encontrado para o artefato selecionado.")
