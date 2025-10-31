# ==============================
# pages/01_🔧 Insumos.py  –  SynapseNext / SAAB TJSP
# ==============================

import sys, os
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

import streamlit as st
from datetime import datetime
from io import BytesIO
from pathlib import Path
import docx2txt, fitz  # PyMuPDF

# ==========================================================
# 🔍 Importações compatíveis (atualizadas)
# ==========================================================
try:
    from utils.integration_insumos import processar_insumo_dinamico
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except ModuleNotFoundError:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sys.path.insert(0, base_dir)
    from utils.integration_insumos import processar_insumo_dinamico
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

        st.info(f"📄 Processando insumo para o artefato **{artefato}**...")

        try:
            resultado = processar_insumo_dinamico(arquivo, artefato)
            if "erro" not in resultado:
                st.success(f"Insumo '{arquivo.name}' processado e encaminhado com sucesso para {artefato}.")
                st.session_state[f"last_insumo_{artefato.lower()}"] = {
                    "nome": arquivo.name,
                    "artefato": artefato,
                    "usuario": usuario,
                    "descricao": descricao,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "resultado": resultado
                }

                # Redireciona automaticamente para o módulo selecionado (caso seja suportado)
                if artefato in ["DFD", "ETP", "TR"]:
                    try:
                        st.switch_page(f"pages/{artefato.lower()}.py")
                    except Exception:
                        st.info(f"📎 Você pode agora abrir o módulo **{artefato}** para revisar os campos.")
            else:
                st.error(f"Erro: {resultado['erro']}")

        except Exception as e:
            st.error(f"Erro no processamento do insumo: {e}")

# ==========================================================
# 🗂️ Histórico de uploads
# ==========================================================
st.divider()
st.subheader("🗂️ Histórico de Insumos (Sessão Atual)")

if "last_insumo_dfd" in st.session_state:
    st.markdown("#### 📘 DFD")
    st.json(st.session_state["last_insumo_dfd"])

if "last_insumo_etp" in st.session_state:
    st.markdown("#### 📗 ETP")
    st.json(st.session_state["last_insumo_etp"])

if "last_insumo_tr" in st.session_state:
    st.markdown("#### 📙 TR")
    st.json(st.session_state["last_insumo_tr"])

st.caption("📎 O histórico é temporário e será limpo ao reiniciar a sessão.")
