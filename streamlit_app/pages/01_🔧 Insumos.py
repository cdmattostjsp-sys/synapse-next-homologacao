# ==============================
# pages/01_🔧 Insumos.py  –  SynapseNext / SAAB TJSP
# ==============================

import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
import sys, os, docx2txt, fitz  # PyMuPDF

# ==========================================================
# 🔍 Importações compatíveis
# ==========================================================
try:
    from utils.integration_insumos import salvar_insumo, listar_insumos, processar_insumo
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except ModuleNotFoundError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, base_dir)
    from utils.integration_insumos import salvar_insumo, listar_insumos, processar_insumo
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração
# ==========================================================
st.set_page_config(page_title="🔧 Insumos", layout="wide", page_icon="🔧")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "🔧 Upload de Insumos Institucionais",
    "Integração inteligente entre artefatos e dados do SynapseNext"
)
st.divider()

# ==========================================================
# 📘 Descrição funcional
# ==========================================================
st.markdown("""
O módulo **INSUMOS** permite anexar documentos institucionais (DFD, ETP, TR, Edital, Contrato)  
que servirão de base para os artefatos gerados automaticamente pelo SynapseNext.  
Cada upload é registrado e o conteúdo pode ser processado semanticamente pela IA  
para preenchimento inteligente do artefato correspondente.
""")

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

arquivo = st.file_uploader("Selecione o arquivo (DOCX, PDF, TXT etc.)", type=["docx", "pdf", "txt"])

# ==========================================================
# 🧾 Processamento do upload
# ==========================================================
if arquivo and st.button("📤 Enviar insumo"):
    with st.spinner("Salvando e processando o documento..."):
        caminho_salvo = salvar_insumo(arquivo, artefato)
        st.success(f"Insumo '{arquivo.name}' salvo com sucesso em {caminho_salvo}")

        # Extração preliminar de texto
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

        # Processamento com IA e parser institucional
        campos_ai = {}
        if texto_extraido.strip():
            try:
                st.info("🤖 IA processando o insumo e identificando campos relevantes...")
                campos_ai = processar_insumo(arquivo, artefato)
            except Exception as e:
                st.error(f"Erro no processamento IA: {e}")
        else:
            st.warning("⚠️ Não foi possível extrair texto legível do arquivo enviado.")

        # ======================================================
        # 💾 Registro seletivo por artefato
        # ======================================================
        chave = f"last_insumo_{artefato.lower()}"
        st.session_state[chave] = {
            "nome": arquivo.name,
            "artefato": artefato,
            "conteudo": (texto_extraido or "")[:100000],
            "campos_ai": campos_ai or {},
            "usuario": usuario,
            "descricao": descricao,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        st.success(f"📎 Insumo armazenado e disponível para o artefato **{artefato}**.")

# ==========================================================
# 🗂️ Histórico de uploads
# ==========================================================
st.divider()
st.subheader("🗂️ Histórico de Insumos Enviados")

artefato_hist = st.selectbox("Filtrar por artefato", ["Todos", "DFD", "ETP", "TR", "EDITAL", "CONTRATO"])

if artefato_hist == "Todos":
    for tipo in ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]:
        arquivos = listar_insumos()
        st.markdown(f"#### 📘 {tipo}")
        st.write(arquivos or "— sem arquivos —")
else:
    arquivos = listar_insumos()
    st.markdown(f"#### 📘 {artefato_hist}")
    st.write(arquivos or "Nenhum insumo encontrado para o artefato selecionado.")
